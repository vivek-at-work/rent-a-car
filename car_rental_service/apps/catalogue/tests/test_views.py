from catalogue.models import Car
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import (APIClient, APIRequestFactory, APITestCase,
                                 force_authenticate)

from .fixtures import (ADMIN_CONTACT, CAR_DATA, CONTACT_NUMBER, NAME, PASSWORD,
                       VALID_DOB)

USER = get_user_model()



class CarAPITests(APITestCase):
    customer = None
    admin = None

    def setUp(self):
        self.customer = USER.objects.create_user(
            NAME, VALID_DOB, CONTACT_NUMBER, PASSWORD
        )
        self.admin = USER.objects.create_superuser(
            NAME, VALID_DOB, ADMIN_CONTACT, PASSWORD
        )

    def test_admin_can_create_car(self):
        url = reverse('car-list')
        payload = CAR_DATA
        self.client.login(username=ADMIN_CONTACT, password=PASSWORD)
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_400_for_bad_payload_while_create_car(self):
        url = reverse('car-list')
        payload = {}
        self.client.login(username=ADMIN_CONTACT, password=PASSWORD)
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_can_not_create_car(self):
        url = reverse('car-list')
        payload = CAR_DATA
        self.client.login(username=CONTACT_NUMBER, password=PASSWORD)
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_customer_can_list_cars(self):
        url = reverse('car-list')
        self.client.login(username=CONTACT_NUMBER, password=PASSWORD)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_customer_can_rent_car(self):
        # Login as admin an create new car
        car_list_url = reverse('car-list')
        payload = CAR_DATA
        self.client.login(username=ADMIN_CONTACT, password=PASSWORD)
        response = self.client.post(car_list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Login as customer and rent the car created by admin
        last_obj = Car.objects.last()
        reserve_url = reverse('car-rent', args=[last_obj.id])
        payload = {'valid_from': timezone.now()}
        self.client.login(username=CONTACT_NUMBER, password=PASSWORD)
        reserve_response = self.client.post(reserve_url, payload, format='json')
        self.assertEqual(reserve_response.status_code, status.HTTP_201_CREATED)

        # Trying to book the same car again
        reserve_response = self.client.post(reserve_url, payload, format='json')
        self.assertEqual(reserve_response.status_code, status.HTTP_404_NOT_FOUND)

        # Login as customer and check if booking is created
        bookings_list_url = reverse('booking-list')
        bookings_list_response = self.client.get(bookings_list_url, format='json')
        assert len(bookings_list_response.data) == 1

    def test_400_for_bad_payload_while_rent_car(self):
        car_list_url = reverse('car-list')
        payload = CAR_DATA
        self.client.login(username=ADMIN_CONTACT, password=PASSWORD)
        response = self.client.post(car_list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Login as customer and rent the car created by admin
        last_obj = Car.objects.last()
        reserve_url = reverse('car-rent', args=[last_obj.id])
        payload = {}
        self.client.login(username=CONTACT_NUMBER, password=PASSWORD)
        reserve_response = self.client.post(reserve_url, payload, format='json')
        self.assertEqual(reserve_response.status_code, status.HTTP_400_BAD_REQUEST)

        # Login as customer and check if booking is created
        bookings_list_url = reverse('booking-list')
        bookings_list_response = self.client.get(bookings_list_url, format='json')
        assert len(bookings_list_response.data) == 0
