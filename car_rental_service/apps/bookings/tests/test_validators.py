from bookings.validators import (PRESENT_OR_FUTURE, PRESENT_OR_PAST,
                                 date_validator)
from django.core.exceptions import ValidationError
from django.test import TestCase

from .fixtures import FUTURE, NOW, PAST


class DateValidatorTestCase(TestCase):
    def test_validates_future_date(self):
        date_validator(PRESENT_OR_FUTURE)(FUTURE)

    def test_validates_raises_exception_past_date(self):
        with self.assertRaises(ValidationError):
            date_validator(PRESENT_OR_FUTURE)(PAST)

    def test_validates_PAST_date(self):
        date_validator(PRESENT_OR_PAST)(PAST)

    def test_validates_raises_exception_future_date(self):
        with self.assertRaises(ValidationError):
            date_validator(PRESENT_OR_PAST)(FUTURE)

    def test_validates_now_present_or_future(self):
        date_validator(PRESENT_OR_FUTURE, NOW)(NOW)

    def test_validates_now_present_or_past(self):
        date_validator(PRESENT_OR_PAST, NOW)(NOW)
