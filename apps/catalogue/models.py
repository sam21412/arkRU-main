from django.db import models
from decimal import Decimal
from oscar.apps.catalogue.abstract_models import AbstractAttributeOption
from oscar.core.loading import is_model_registered

__all__ = []

if not is_model_registered('catalogue', 'AttributeOption'):
    class AttributeOption(AbstractAttributeOption):
        price = models.DecimalField(
            'Price', 
            decimal_places=2, 
            max_digits=12,
            default=Decimal('0.00'), 
            blank=True
        )

        class Meta:
            app_label = 'catalogue'
            
    __all__.append('AttributeOption')

# Импортируем все остальные модели Oscar
from oscar.apps.catalogue.models import *  # noqa isort:skip
