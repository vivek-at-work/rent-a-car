from customers.managers import CustomerManager
from customers.validators import (validate_contact_number,
                                  validate_date_of_birth)
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(AbstractBaseUser):
    name = models.CharField(max_length=255)
    contact_number = models.CharField(
        max_length=10,
        unique=True,
        validators=[validate_contact_number],
        help_text=_('Contact Numbers that should start with one of [789] and max length to be 10 digits'),
    )
    date_of_birth = models.DateField(
        validators=[validate_date_of_birth],
        help_text=_(
            'Date of birth of customer validation to check if user is above 18 years of age.'),
                                     )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'contact_number'
    REQUIRED_FIELDS = ['name', 'date_of_birth']

    objects = CustomerManager()

    def has_perm(self, perm, obj=None):
        """
        Deny All Permissions to Staff User
        """
        return self.is_superuser

    def has_module_perms(self, app_label):
        """
        Deny All Module Level Permissions to Staff User
        """
        return self.is_superuser

    def __str__(self):
        return self.contact_number
