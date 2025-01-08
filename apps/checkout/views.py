from oscar.apps.checkout import views
from yookassa import Configuration, Payment
import uuid
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from yookassa.domain.notification import WebhookNotification
import json
from decimal import Decimal
from oscar.core.loading import get_class, get_model
from django.db import transaction
import logging
import stripe

logger = logging.getLogger(__name__)

Order = get_model('order', 'Order')
OrderCreator = get_class('order.utils', 'OrderCreator')

class PaymentDetailsView(views.PaymentDetailsView):
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Добавляем оба ключа в контекст независимо от выбранного метода
        payment_method = self.request.session.get('payment_method', '')
        ctx['payment_token'] = None
        ctx['stripe_session_url'] = None
        
        # Если метод уже выбран, генерируем соответствующую ссылку
        if payment_method == 'yookassa':
            ctx['payment_token'] = self.generate_yookassa_payment()
        elif payment_method == 'stripe':
            ctx['stripe_session_url'] = self.generate_stripe_payment()
            
        ctx['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
        return ctx

    def post(self, request, *args, **kwargs):
        payment_method = request.POST.get('payment_method')
        if payment_method:
            request.session['payment_method'] = payment_method
            if payment_method == 'yookassa':
                payment_token = self.generate_yookassa_payment()
                return redirect(payment_token)
            elif payment_method == 'stripe':
                stripe_session_url = self.generate_stripe_payment()
                return redirect(stripe_session_url)
                
        return super().post(request, *args, **kwargs)

    def handle_payment_selection(self, request):
        payment_method = request.POST.get('payment_method')
        request.session['payment_method'] = payment_method
        return self.get_success_response()

    def generate_payment(self):
        payment_method = self.request.session.get('payment_method', 'yookassa')
        
        if payment_method == 'yookassa':
            return self.generate_yookassa_payment()
        elif payment_method == 'stripe':
            return self.generate_stripe_payment()

    def generate_yookassa_payment(self):
        Configuration.account_id = settings.YOOKASSA_SHOP_ID
        Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

        # Получаем submission из формы
        submission = self.build_submission()
        order_total = submission['order_total']
        
        # Убедимся что цена корректно преобразована
        total_str = "{:.2f}".format(float(order_total.incl_tax))
        
        # Сохраняем сумму в сессии для последующей проверки
        self.request.session['payment_amount'] = total_str

        payment = Payment.create({
            "amount": {
                "value": total_str,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": self.request.build_absolute_uri(reverse('checkout:thank-you'))
            },
            "capture": True,
            "description": f"Заказ {self.request.basket.id}",
            "metadata": {
                "order_id": str(self.request.basket.id),
                "order_total": total_str,
                "payment_amount": total_str  # Добавляем сумму в метаданные
            }
        }, uuid.uuid4())

        # Сохраняем ID платежа в сессии
        self.request.session['payment_id'] = payment.id
        return payment.confirmation.confirmation_url

    def generate_stripe_payment(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        submission = self.build_submission()
        order_total = submission['order_total']
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(float(order_total.incl_tax) * 100),
                    'product_data': {
                        'name': f'Order {self.request.basket.id}',
                    },
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=self.request.build_absolute_uri(reverse('checkout:thank-you')),
            cancel_url=self.request.build_absolute_uri(reverse('checkout:payment-details')),
        )
        
        return session.url

    @transaction.atomic
    def handle_payment(self, order_number, total, **kwargs):
        """
        Обработка платежа и сохранение информации о транзакции
        """
        # Получаем payment_token из сессии или другого источника
        submission = self.build_submission()
        
        # Убедимся, что total совпадает с суммой заказа
        if total.incl_tax != submission['order_total'].incl_tax:
            total = submission['order_total']
        
        # Возвращаем None, так как платеж обрабатывается на стороне ЮKassa
        return None

    def handle_successful_order(self, order):
        """
        Обработка успешного заказа
        """
        # Сохраняем информацию о платеже в заказе
        order.payment_method = "YooKassa"
        order.save()
        return super().handle_successful_order(order)

class ThankYouView(views.ThankYouView):
    """
    Отображение страницы благодарности после оплаты
    """
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        # Получаем информацию о платеже
        payment_id = self.request.session.get('payment_id')
        if payment_id:
            try:
                Configuration.account_id = settings.YOOKASSA_SHOP_ID
                Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
                payment = Payment.find_one(payment_id)
                
                ctx.update({
                    'payment_amount': payment.amount.value,
                    'payment_currency': payment.amount.currency,
                    'payment_status': payment.status,
                })
            except Exception as e:
                logger.error(f"Error getting payment info: {e}")
                
        return ctx

@csrf_exempt
def yookassa_webhook(request):
    event_json = json.loads(request.body)
    try:
        notification = WebhookNotification(event_json)
        payment = notification.object
        
        if payment.status == 'succeeded':
            order_id = payment.metadata.get('order_id')
            paid_amount = Decimal(payment.amount.value)
            
            order = Order.objects.get(number=order_id)
            order.payment_amount = paid_amount
            order.payment_currency = payment.amount.currency
            order.payment_method = 'YooKassa'
            order.payment_id = payment.id
            order.status = 'Paid'
            order.save()
            
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return HttpResponse(status=400)
    
    return HttpResponse(status=200)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
        
        logger.info(f"Received Stripe webhook: {event['type']}")
        
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            logger.info(f"Processing successful payment for order: {session.metadata.get('order_id')}")
            
            order_id = session.metadata.get('order_id')
            
            order = Order.objects.get(number=order_id)
            order.payment_method = 'Stripe'
            order.payment_id = session.payment_intent
            order.payment_amount = Decimal(session.amount_total) / 100
            order.payment_currency = session.currency.upper()
            order.status = 'Paid'
            order.save()
            
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {str(e)}")
        return HttpResponse(status=400)
    except Exception as e:
        logger.error(f'Stripe webhook error: {str(e)}')
        return HttpResponse(status=400)
        
    return HttpResponse(status=200)
