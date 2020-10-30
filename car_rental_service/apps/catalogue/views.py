import logging

from bookings.models import Booking
from bookings.serializers import BookingSerializer
from calculators import booking_number_generator
from catalogue.models import Car
from django.db import IntegrityError, transaction
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import CarSerializer, RentACarSerializer

logger = logging.getLogger(__name__)


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class CarViewSet(viewsets.ModelViewSet):
    """
    Model view set for car listing and booking
    """

    queryset = Car.available_objects.all()
    serializer_class = CarSerializer
    # READ ONLY FOR CUSTOMERS
    permission_classes = [permissions.IsAdminUser | ReadOnly]

    @action(
        detail=True,
        serializer_class=RentACarSerializer,
        permission_classes=[permissions.IsAuthenticated],
        methods=['post'],
    )
    def rent(self, request, pk):
        """
        rent action to renting a car
        """
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request},
        )
        if serializer.is_valid():
            car = self.get_object()
            try:
                with transaction.atomic():
                    booking = Booking.objects.create(
                        car=car,
                        customer=request.user,
                        applicable_base_rental_rate=car.base_day_rental,
                        applicable_par_kilometer_price=car.per_kilometer_price,
                        initial_milage=car.current_milage,
                        booking_number=booking_number_generator(5),
                        **serializer.validated_data
                    )
                    car.is_hired = True
                    car.save()
                    logger.info(
                        'New booking %s is created and car %s now unavilable for next bookings',
                        booking,
                        request.user,
                    )
            except IntegrityError as err:
                logger.error(
                    'Something went wrong while creating the booking for car %s as err %s.',
                    booking,
                    err,
                )
                return Response(
                    {'error': _('Could not rent this car.')},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                BookingSerializer(booking, context={'request': request}).data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
