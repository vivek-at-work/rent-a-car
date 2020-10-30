from authentication.backends import ConatctNumberBasedAuthenticationsBackend
from django.urls import exceptions, reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .fixtures import *


class CustomersAPITests(APITestCase):
    def test_customer_sign_up(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse('customer-register')
        payload = {
            'name': NAME,
            'date_of_birth': VALID_DOB,
            'contact_number': CONTACT_NUMBER,
            'password': PASSWORD,
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        t = ConatctNumberBasedAuthenticationsBackend().authenticate(
            {}, username=CONTACT_NUMBER, password=PASSWORD,
        )
        assert str(t) == CONTACT_NUMBER

    def test_customer_list(self):
        """
        Ensure we can create a new customer object and get the same in list.
        """
        sign_up_url = reverse('customer-register')
        payload = {
            'name': NAME,
            'date_of_birth': VALID_DOB,
            'contact_number': CONTACT_NUMBER,
            'password': PASSWORD,
        }
        sign_up_response = self.client.post(
            sign_up_url, payload, format='json')
        self.assertEqual(sign_up_response.status_code, status.HTTP_201_CREATED)
        t = ConatctNumberBasedAuthenticationsBackend().authenticate(
            {}, username=CONTACT_NUMBER, password=PASSWORD,
        )
        self.client.login(username=CONTACT_NUMBER, password=PASSWORD)
        list_url = reverse('customer-list')
        list_response = self.client.get(list_url, format='json')
        assert len(list_response.data) == 1

    def test_duplicate_user_sign_up(self):
        """
        Ensure we can register a new user object with a unique  contact number
        once only
        """
        sign_up_url = reverse('customer-register')
        payload = {
            'name': NAME,
            'date_of_birth': VALID_DOB,
            'contact_number': CONTACT_NUMBER,
            'password': PASSWORD,
        }
        sign_up_response = self.client.post(
            sign_up_url, payload, format='json')
        self.assertEqual(sign_up_response.status_code, status.HTTP_201_CREATED)
        duplicate_sign_up_response = self.client.post(
            sign_up_url, payload, format='json')
        self.assertEqual(duplicate_sign_up_response.status_code,
                         status.HTTP_400_BAD_REQUEST)


    def test_post_is_not_availabe(self):
        """
        Ensure we can register a new user object with a unique  contact number
        once only
        """
        with self.assertRaises(exceptions.NoReverseMatch):
            reverse('customer-create')
