from authentication.bearer_token import BearerTokenAuthentication
from django.test import TestCase


class BearerTokenAuthenticationTestCase(TestCase):
    def test_key(self):
        """Test Existing Customers can login"""
        assert BearerTokenAuthentication.keyword == 'Bearer'
