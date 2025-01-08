from django.db import models
from oscar.apps.order.abstract_models import AbstractOrder

class Order(AbstractOrder):
    payment_method = models.CharField(max_length=128, blank=True)
    payment_id = models.CharField(max_length=128, blank=True)
    payment_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        verbose_name='Payment Amount'
    )
    payment_currency = models.CharField(
        max_length=12, 
        default='RUB',
        verbose_name='Payment Currency'
    )

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

from oscar.apps.order.models import *  # noqa isort:skip
