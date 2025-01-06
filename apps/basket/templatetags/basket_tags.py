from django import template
from oscar.apps.basket.forms import AddToBasketForm

register = template.Library()

@register.simple_tag(takes_context=True)
def basket_form(context, product):
    request = context['request']
    initial = {}
    form = AddToBasketForm(request.basket, product=product, initial=initial)
    return form
