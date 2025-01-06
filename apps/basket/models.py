from decimal import Decimal
from oscar.apps.basket.abstract_models import AbstractLine
from oscar.core.loading import get_model
from django.db import models

AttributeOption = get_model('catalogue', 'AttributeOption')

class Line(AbstractLine):
    def get_options_multiplier(self):
        """
        Вычисляет общий множитель цены из опций для строки
        """
        multiplier = Decimal('1.00')  # Начальное значение множителя
        if hasattr(self, 'attributes'):
            for attr in self.attributes.all():
                try:
                    option = AttributeOption.objects.get(option=attr.value)
                    if option.price:
                        # Прибавляем к множителю процент от цены (например, 1.5 = +50% к цене)
                        multiplier *= Decimal('1.00') + (Decimal(str(option.price)) / Decimal('100.00'))
                except AttributeOption.DoesNotExist:
                    continue
        return multiplier

    @property
    def unit_price_incl_tax(self):
        base_price = super().unit_price_incl_tax
        return base_price * self.get_options_multiplier()

    @property
    def unit_price_excl_tax(self):
        base_price = super().unit_price_excl_tax
        return base_price * self.get_options_multiplier()

    # Для общей цены строки используем unit_price, который уже включает стоимость опций
    @property
    def line_price_incl_tax(self):
        return self.unit_price_incl_tax * self.quantity

    @property
    def line_price_excl_tax(self):
        return self.unit_price_excl_tax * self.quantity

from oscar.apps.basket.models import *  # noqa isort:skip
