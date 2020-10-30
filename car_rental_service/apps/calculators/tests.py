from django.test import TestCase

from .booking_number_generator import booking_number_generator
from .exceptions import RequiredArgumentNotAvailableError
from .price_calculators import (CompactCarPriceCalculator,
                                MiniVanPriceCalculator,
                                PremiumCarPriceCalculator)


class CompactCarPriceCalculatorTestCase(TestCase):
    def test_compact_car_caluclator(self):
        """test compact car price calculation"""
        price = CompactCarPriceCalculator().calculate(10, 2)
        assert price == float(20)


class PremiumCarPriceCalculatorTestCase(TestCase):
    def test_positive(self):
        """test premium car price calculation"""
        price = PremiumCarPriceCalculator().calculate(
            10, 2, per_km_price=1, number_of_kilo_meters=2
        )
        assert price == round(26.0, 2)

    def test_negative(self):
        """test exception if required arguments not provided"""
        with self.assertRaises(RequiredArgumentNotAvailableError):
            price = PremiumCarPriceCalculator().calculate(10, 2)
            assert price == round(26.0, 2)


class MiniVanPriceCalculatorTestCase(TestCase):
    def test_positive(self):
        """test minivan car price calculation"""
        price = MiniVanPriceCalculator().calculate(
            10, 2, per_km_price=1, number_of_kilo_meters=2
        )
        assert price == round(37.0, 2)

    def test_negative(self):
        """test exception if required arguments not provided"""
        with self.assertRaises(RequiredArgumentNotAvailableError):
            price = PremiumCarPriceCalculator().calculate(10, 2)
            assert price == round(26.0, 2)


class BookingNumberGeneratorTestCase(TestCase):
    def test_defaults(self):
        """Test booking_number_generator with defult length"""
        assert len(booking_number_generator()) == 6

    def test_specific_length(self):
        """Test booking_number_generator with specific length"""
        assert len(booking_number_generator(4)) == 4
