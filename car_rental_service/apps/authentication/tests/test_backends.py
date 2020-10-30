from authentication.backends import ConatctNumberBasedAuthenticationsBackend
from django.contrib.auth import get_user_model
from django.test import TestCase

from .fixtures import VALID_USER_DATA

USER = get_user_model()

class ConatctNumberBasedAuthenticationsBackendTestCase(TestCase):
    def setUp(self):
        USER.objects.create_user(**VALID_USER_DATA)

    def test_customer_login(self):
        """Test Existing Customers can login"""
        user = ConatctNumberBasedAuthenticationsBackend().authenticate(
            {}, username=VALID_USER_DATA['contact_number'], password=VALID_USER_DATA['password'],
        )
        assert str(user) == VALID_USER_DATA['contact_number']

    def test_non_customer_login(self):
        """Test Non Existing Customers can not login"""
        customer = ConatctNumberBasedAuthenticationsBackend().authenticate(
            {}, username=VALID_USER_DATA['contact_number'][::-1], password=VALID_USER_DATA['password'],
        )
        assert customer is None
