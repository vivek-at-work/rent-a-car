from calculators import (CompactCarPriceCalculator, MiniVanPriceCalculator,
                         PremiumCarPriceCalculator)
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .car_categories import CarCategories
from .exceptions import (IncorrectBaseRateError,
                         IncorrectParKilometerPriceError,
                         PriceCalculatorNotFoundError)
from .querysets import AvailabelCarQuerySet


class Car(models.Model):
    """
    An Individual Car available for rental.
    """

    price_calculators = {
        CarCategories.COMPACT: CompactCarPriceCalculator,
        CarCategories.PREMIUM: PremiumCarPriceCalculator,
        CarCategories.MINIVAN: MiniVanPriceCalculator,
    }

    category = models.IntegerField(
        choices=CarCategories.choices,
        default=CarCategories.PREMIUM,
        help_text=_('To which category of cars this individual car belongs to.'),
    )

    number = models.CharField(
        max_length=10,
        unique=True,
        null = False,
        help_text=_('An human readable unique identifier or number for this car.'),
    )

    is_hired = models.BooleanField(
        default=False,
        help_text=_(
            """Represents this car is currently hired if set to true otherwise false"""
        ),
    )

    current_milage = models.FloatField(
        null = False,
        help_text=_("""Represents the current milage of the car""")
    )

    objects = models.Manager()
    available_objects = AvailabelCarQuerySet.as_manager()

    @property
    def base_day_rental(self):
        """returns base dey rental for this car

        Raises:
            IncorrectBaseRateError: raised if incorrect base rental value is set

        Returns:
            [float]: [base dey rental value]
        """

        try:
            value = settings.BASE_DAY_RENTAL
            return float(value)
        except ValueError:
            raise IncorrectBaseRateError(settings.BASE_DAY_RENTAL)

    @property
    def per_kilometer_price(self):
        """Per Kilometer Price for this car

        Raises:
            IncorrectParKilometerPriceError: raised if incorrect per km price value is set

        Returns:
            [float]: [per km price value]
        """
        try:
            value = settings.PER_KILOMETER_PRICE
            return float(value)
        except ValueError:
            raise IncorrectParKilometerPriceError(settings.PER_KILOMETER_PRICE)

    @property
    def rental_calculator(self):
        """Rental Calculator for this car
        Raises:
            PriceCalculatorNotFoundError: raised if price calculator is not found for the car

        Returns:
            [BasePriceCalculator]: [calculator for the car type]
        """
        try:
            return self.price_calculators[self.category]()
        except ex:
            raise PriceCalculatorNotFoundError(self.category)

    def __str__(self):
        return self.number
