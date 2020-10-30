from rest_framework import serializers

from .models import Booking


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    """
    BookingSerializer is used for serializing booking or  list of bookings.
    """
    is_closed = serializers.BooleanField(read_only=True)
    class Meta:
        model = Booking
        fields = (
            'url',
            'car',
            'customer',
            'valid_from',
            'initial_milage',
            'applicable_base_rental_rate',
            'applicable_par_kilometer_price',
            'booking_number',
            'returned_at',
            'last_milage',
            'payable_amount',
            'is_closed'
        )


class BookingCloseSerializer(serializers.Serializer):
    """
    BookingCloseSerializer is used for validating the payload
    while user returns the car.
    """

    returned_at = serializers.DateTimeField()
    last_milage = serializers.FloatField()
