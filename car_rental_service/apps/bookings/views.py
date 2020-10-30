import logging

from django.db import IntegrityError, transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .exceptions import BookingClosedError
from .models import Booking
from .serializers import BookingCloseSerializer, BookingSerializer

logger = logging.getLogger(__name__)


class BookingsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read Only Model view set for listing down booking  and close a booking
    A Customer can only view booking that he owns
    """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(
        detail=True,
        serializer_class=BookingCloseSerializer,
        methods=['post'],
    )
    def close(self, request, pk):
        """
        Custom action to be called when a customer wants to
        close his booking for a car.
        """
        booking = self.get_object()
        logger.info('Request Received for closing a booking %s .', booking)
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request},
        )
        if serializer.is_valid():
            if booking.is_closed:
                raise BookingClosedError(booking)
            booking.close(**serializer.validated_data)
            try:
                with transaction.atomic():
                    booking.save()
                    car = booking.car
                    car.current_milage = booking.last_milage
                    car.is_hired = False
                    car.save()
                    logger.info(
                        'booking %s is closed now and car is available %s for further bookings  ',
                        booking,
                        car,
                    )
            except IntegrityError as err:
                logger.error(
                    'Something went wrong while closing the booking %s due to %s.',
                    booking,
                    err,
                )
                return Response(
                    {'error': _('Could not close this booking.')},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                BookingSerializer(booking, context={'request': request}).data,
                status=status.HTTP_202_ACCEPTED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(customer=self.request.user)
