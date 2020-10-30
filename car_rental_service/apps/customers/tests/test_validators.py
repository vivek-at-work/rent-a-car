from customers.validators import (validate_contact_number,
                                  validate_date_of_birth)
from django.core.exceptions import ValidationError
from django.test import TestCase

from .fixtures import *


class ValidatorsTestCase(TestCase):

    def test_invalid_contact_number(self):
        """Test  Invalid contact number results to validation error"""
        with self.assertRaises(ValidationError):
            validate_contact_number(INVALID_CONTACT_NUMBER)

    def test_valid_contact_number(self):
        """Test valid contact number results to no validation error"""
        validate_contact_number(CONTACT_NUMBER)

    def test_invalid_date_of_birth(self):
        """Test invalid Date of birth results to validation error"""
        with self.assertRaises(ValidationError):
            validate_date_of_birth(INVALID_DOB)

    def test_valid_date_of_birth(self):
        """Test valid Date of birth results to no validation error"""
        validate_date_of_birth(VALID_DOB)
