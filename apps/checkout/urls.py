from django.urls import path
from . import views

urlpatterns = [
    # ...existing urls...
    path('yookassa-webhook/', views.yookassa_webhook, name='yookassa-webhook'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe-webhook'),
]