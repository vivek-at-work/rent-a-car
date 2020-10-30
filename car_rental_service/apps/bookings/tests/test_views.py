from bookings.models import Booking
from calculators import booking_number_generator
from catalogue.models import Car
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import (APIClient, APIRequestFactory, APITestCase,
                                 force_authenticate)

from .fixtures import CAR_DATA, CUSTOMER_DATA, CUSTOMER_DATA_TWO, NOW

USER = get_user_model()


class BookingAPITests(APITestCase):
    customers = []
    car = None

    def setUp(self):
        self.car = Car.objects.create(**CAR_DATA)
        self.customers = [
            USER.objects.create_user(**CUSTOMER_DATA),
            USER.objects.create_user(**CUSTOMER_DATA_TWO),
        ]

    def test_customer_can_list_own_bookings(self):
        for customer in self.customers:
            Booking.objects.create(
                car=self.car,
                customer=customer,
                applicable_base_rental_rate=10,
                applicable_par_kilometer_price=5,
                valid_from=NOW,
                booking_number=booking_number_generator(3),
                initial_milage=1,
            )
        url = reverse('booking-list')
        self.client.login(
            username=CUSTOMER_DATA['contact_number'], password=CUSTOMER_DATA['password']
        )
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert len(response.data) == 1

    def test_customer_can_cancel_a_booking(self):
        customer = self.customers[0]
        Booking.objects.create(
            car=self.car,
            customer=customer,
            applicable_base_rental_rate=10,
            applicable_par_kilometer_price=5,
            valid_from=NOW,
            booking_number=booking_number_generator(3),
            initial_milage=1,
        )
        last_obj = Booking.objects.last()
        payload = {'returned_at': NOW, 'last_milage': 20}
        reserve_url = reverse('booking-close', args=[last_obj.id])
        self.client.login(
            username=CUSTOMER_DATA['contact_number'], password=CUSTOMER_DATA['password']
        )
        reserve_response = self.client.post(reserve_url, payload, format='json')
        self.assertEqual(reserve_response.status_code, status.HTTP_202_ACCEPTED)
