from bookings.exceptions import BookingClosedError, ReturnDataNotAvailableError
from bookings.models import Booking
from catalogue.models import Car
from django.contrib.auth import get_user_model
from django.db import transaction, utils
from django.test import TestCase

from .fixtures import CAR_DATA, CUSTOMER_DATA, FUTURE, NOW


class BookingTestCase(TestCase):
    car = None
    customer = None

    def setUp(self):
        self.car = Car.objects.create(**CAR_DATA)
        self.customer = get_user_model().objects.create_user(**CUSTOMER_DATA)

    def create_new_booking(self):
        return Booking.objects.create(
            car=self.car,
            customer=self.customer,
            applicable_base_rental_rate=10,
            applicable_par_kilometer_price=5,
            valid_from=NOW,
            initial_milage=1)

    def test_can_create_bookings(self):
        self.create_new_booking()

    def test_required_fields_to_create_bookings(self):

        with transaction.atomic():
            with self.assertRaises(utils.IntegrityError):
                Booking.objects.create(
                    customer=self.customer,
                    applicable_base_rental_rate=10,
                    applicable_par_kilometer_price=5,
                    valid_from=NOW,
                )
        with transaction.atomic():
            with self.assertRaises(utils.IntegrityError):
                Booking.objects.create(
                    car=self.car,
                    applicable_base_rental_rate=10,
                    applicable_par_kilometer_price=5,
                    valid_from=NOW,
                )
        with transaction.atomic():
            with self.assertRaises(utils.IntegrityError):
                Booking.objects.create(
                    car=self.car,
                    customer=self.customer,
                    applicable_par_kilometer_price=5,
                    valid_from=NOW,
                )
        with transaction.atomic():
            with self.assertRaises(utils.IntegrityError):
                Booking.objects.create(
                    car=self.car,
                    customer=self.customer,
                    applicable_base_rental_rate=10,
                    valid_from=NOW,
                )
        with transaction.atomic():
            with self.assertRaises(utils.IntegrityError):
                Booking.objects.create(
                    car=self.car,
                    customer=self.customer,
                    applicable_base_rental_rate=10,
                    applicable_par_kilometer_price=5,
                )


    def test_is_closed_is_false_for_new_bookings(self):
        booking = self.create_new_booking()
        assert booking.is_closed == False

    def test_can_close_a_bookings(self):
        booking = self.create_new_booking()
        assert booking.is_closed == False
        booking.close(self.car.current_milage + 1, FUTURE)
        assert booking.is_closed == True
        assert booking.payable_amount == 61.0

    def test_exception_while_acessing_duration_non_closed_booking(self):
        booking = self.create_new_booking()
        with self.assertRaises(ReturnDataNotAvailableError):
            booking.duration
        with self.assertRaises(ReturnDataNotAvailableError):
            booking.distance_covered
        booking.close(self.car.current_milage + 1, FUTURE)
        assert booking.duration is not None

    def test_exception_on_closing_a_closed_booking(self):
        booking = self.create_new_booking()
        booking.close(self.car.current_milage + 1, FUTURE)
        with self.assertRaises(BookingClosedError):
            booking.close(self.car.current_milage + 1, FUTURE)
