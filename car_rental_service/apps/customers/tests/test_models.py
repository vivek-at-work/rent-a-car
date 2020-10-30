from django.db import models
from django.test import TestCase

from .fixtures import *


class CustomerTestCase(TestCase):
    def test_customer_fields(self):
        """Test  Customer fields Types"""
        assert type(
            CUSTOMER.name.field) == models.fields.CharField
        assert type(
            CUSTOMER.contact_number.field) == models.fields.CharField
        assert type(
            CUSTOMER.date_of_birth.field) == models.fields.DateField
        assert type(
            CUSTOMER.is_staff.field) == models.fields.BooleanField
        assert type(
            CUSTOMER.is_superuser.field) == models.fields.BooleanField

    def test_customer_username_field(self):
        """Test Customer Username field"""
        assert CUSTOMER.USERNAME_FIELD == 'contact_number'

    def test_customer_required_fields(self):
        """Test  Customer fields Types"""
        assert CUSTOMER.REQUIRED_FIELDS == ['name', 'date_of_birth']
