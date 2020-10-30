from catalogue.car_categories import CarCategories
from django.test import TestCase


class CarCategoriesTestCase(TestCase):

    def test_car_categories(self):
        """Test Car Category Choices"""
        assert CarCategories.choices == [(1, 'Compact'), (2, 'Premium'), (3, 'Minivan')]
