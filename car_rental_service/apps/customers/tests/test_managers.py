from customers.models import Customer
from django.core.exceptions import ValidationError
from django.test import TestCase

from .fixtures import *

CUSTOMER = Customer

class CustomerTestCase(TestCase):
    def test_customer_creation(self):
        """Test Normal Customer Creation"""
        customer = CUSTOMER.objects.create_user(
            NAME, VALID_DOB, CONTACT_NUMBER, PASSWORD)
        assert customer.name == NAME
        assert customer.date_of_birth == VALID_DOB
        assert customer.contact_number == CONTACT_NUMBER
        assert customer.is_staff == False
        assert customer.is_superuser == False
        assert customer.has_perm('', None) == False
        assert customer.has_module_perms('') == False
        assert str(customer) == customer.contact_number

    def test_customer_creation_invalid_date_of_birth(self):
        """Test Normal Customer Creation with invalid Date of birth"""
        with self.assertRaises(ValidationError):
            customer = CUSTOMER.objects.create_user(
                NAME, INVALID_DOB, CONTACT_NUMBER, PASSWORD)

    def test_customer_creation_invalid_contact_number(self):
        """Test Normal Customer Creation with invalid Contact Number"""
        with self.assertRaises(ValidationError):
            customer = CUSTOMER.objects.create_user(
                NAME, VALID_DOB, INVALID_CONTACT_NUMBER, PASSWORD)

    def test_super_Customer_creation(self):
        """Test Super Customer Creation"""
        customer = CUSTOMER.objects.create_superuser(
            NAME, VALID_DOB, CONTACT_NUMBER, PASSWORD)
        assert customer.contact_number == CONTACT_NUMBER
        assert customer.name == NAME
        assert customer.date_of_birth == VALID_DOB
        assert customer.is_staff == True
        assert customer.is_superuser == True
        assert customer.has_perm('', None) == True
        assert customer.has_module_perms('') == True
        assert str(customer) == customer.contact_number
