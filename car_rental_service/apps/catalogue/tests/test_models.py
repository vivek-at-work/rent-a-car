from catalogue.car_categories import CarCategories
from catalogue.models import Car
from django.conf import settings
from django.db import models, transaction, utils
from django.test import TestCase

from .fixtures import CAR_NUMBER


class CarTestCase(TestCase):
    def test_can_read_base_day_rental(self):
        car = Car.objects.create(
            category=CarCategories.PREMIUM, number=CAR_NUMBER, current_milage=10
        )
        assert car.base_day_rental == float(settings.BASE_DAY_RENTAL)

    def test_can_read_per_kilometer_price(self):
        car = Car.objects.create(
            category=CarCategories.PREMIUM, number=CAR_NUMBER, current_milage=10
        )
        assert car.per_kilometer_price == float(settings.PER_KILOMETER_PRICE)

    def test_all_price_calculators_exist(self):
        for x, y in CarCategories.choices:
            car = Car.objects.create(category=x, number=f'{CAR_NUMBER}{x}', current_milage=10)
            assert car.rental_calculator is not None
            assert type(car.rental_calculator) == car.price_calculators[car.category]
