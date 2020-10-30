from customers.validators import (validate_contact_number,
                                  validate_date_of_birth)
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class CustomerManager(BaseUserManager):
    """
    Customer model manager where contact_number is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self,name, date_of_birth, contact_number, password, **extra_fields):
        """
        Create and save an user with the given contact number and password.
        """
        errors = {}
        if not name:
            errors['name'] = _('Name must be set')
        if not date_of_birth:
            errors['date_of_birth'] = _('Date of Birth must be set')
        if not contact_number:
            errors['contact_number'] = _('Contact number must be set')
        if not password:
            errors['password'] = _('Password must be set')
        if errors:
            raise ValidationError(errors)
        validate_date_of_birth(date_of_birth)
        validate_contact_number(contact_number)
        user = self.model(
            name= name,
            date_of_birth=date_of_birth,
            contact_number=contact_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, date_of_birth, contact_number, password, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(name, date_of_birth, contact_number, password, **extra_fields)
