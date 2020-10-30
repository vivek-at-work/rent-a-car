from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_field

from .exceptions import BookingClosedError, ReturnDataNotAvailableError
from .validators import PRESENT_OR_FUTURE, PRESENT_OR_PAST, date_validator


class Booking(models.Model):
    """
    An Booking to track a rental history for a car and customer.
    """

    car = models.ForeignKey(
        'catalogue.Car',
        on_delete=models.PROTECT,
        related_name='bookings',
        help_text=_('Car for which this booking is done.'),
    )

    customer = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        related_name='bookings_owned',
        help_text=_('Customer who owns this booking.'),
    )

    valid_from = models.DateTimeField(
        validators=[date_validator(PRESENT_OR_FUTURE)],
        help_text=_('Time Stamp after which booking is valid.'),
    )

    """We are keeping applicable_base_rental_rate
       and applicable_par_kilometer_price
       here as well because base_rental_rate and
       par_kilometer_price can change which a booking is
       in progress or any time in future"""
    applicable_base_rental_rate = models.FloatField(
        help_text=_('Applicable Base Rental Rate at which the booking was done.'),
    )
    applicable_par_kilometer_price = models.FloatField(
        help_text=_('Applicable Par Kilometer Price at which the booking was done.'),
    )
    booking_number = models.CharField(
        max_length=10,
        unique=True,
        help_text=_('A human readable unique identifier this booking.'),
    )
    initial_milage = models.FloatField(
        help_text=_('Represents the initial milage of the car at the time of booking.'),
    )

    last_milage = models.FloatField(
        null=True, help_text=_('Represents the last milage of the car at return during this booking.')
    )

    returned_at = models.DateTimeField(
        null=True,
        validators=[date_validator(PRESENT_OR_PAST)],
        help_text=_('DateTime stamp at which the car was returned and booking was closed.'),
    )
    payable_amount = models.FloatField(
        null=True, help_text=_('Total Payable Amount for this booking.')
    )

    @property
    def duration(self):
        """Duration of booking in Days

        Raises:
            ReturnDataNotAvailableError: is raised if returned_at is set to None

        Returns:
            float: Number of Days in fraction
        """
        if self.returned_at is None:
            raise ReturnDataNotAvailableError(self, 'Booking return_at is None.')
        delta = self.returned_at - self.valid_from
        return delta.total_seconds() / timedelta(days=1).total_seconds()

    @property
    def distance_covered(self):
        """Distance Covered During this booking

        Raises:
            ReturnDataNotAvailableError: is raised if last_milage is set to None

        Returns:
            float: Number of Kilometer in fraction
        """
        if self.last_milage is None:
            raise ReturnDataNotAvailableError(self, 'Booking last_milage is None.')
        return self.last_milage - self.initial_milage

    @property
    def is_closed(self):
        """Flag that represents if this booking is closed

        Returns:
            Boolean: True if Booking is closed
        """

        return self.returned_at is not None

    def _calculate_payable_amount(self):
        """Its a private method , avoid using from outside
           Calculates the payable amount for this booking

        Returns:
            float: Amount payable for this booking
        """
        return self.car.rental_calculator.calculate(
            self.applicable_base_rental_rate,
            self.duration,
            per_km_price=self.applicable_par_kilometer_price,
            number_of_kilo_meters=self.distance_covered,
        )

    def _validate_last_milage(self, value):
        """Validates that last_milage value
           if it is smaller than initial milage.

        Args:
            value (float): last_milage

        Raises:
            ValidationError: last_milage value can't be smaller than initial milage.
        """
        if value < self.initial_milage:
            raise ValidationError(
                _("last_milage value can't be smaller than initial_milage.")
            )

    def close(self, last_milage, returned_at):
        """This method marks the booking closed.

        Args:
            last_milage (Float): Milage of the car at the time of return.
            returned_at (Datetime): TimeStamp at which car was returned.

        Returns:
            Booking: Returning the self reference just in case we wish make chain of method calls
        """
        if self.is_closed:
            raise BookingClosedError(self)
        self._validate_last_milage(last_milage)
        self.last_milage = last_milage
        date_validator(PRESENT_OR_FUTURE, current_time=self.valid_from)(returned_at)
        self.returned_at = returned_at
        self.payable_amount = self._calculate_payable_amount()
        return self

    def __str__(self):
        return self.booking_number
