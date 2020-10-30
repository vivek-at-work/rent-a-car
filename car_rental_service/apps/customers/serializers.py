from customers.models import (Customer, validate_contact_number,
                              validate_date_of_birth)
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

CUSTOMER = Customer


class SignUpSerializer(serializers.Serializer):
    """
    Sign Up Serializer used for customer sign up request validation
    """
    contact_number = serializers.CharField(
        validators=[validate_contact_number,
                    UniqueValidator(
                        queryset=CUSTOMER.objects.all(),
                        message=_('Contact Number is already registered'))],
    )
    name = serializers.CharField()
    date_of_birth = serializers.DateField(
        validators=[validate_date_of_birth]
    )
    password = serializers.CharField()


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """
    Customer Hyperlinked Model Serializer used for customer listing
    """
    class Meta:
        model = CUSTOMER
        fields = ('url', 'contact_number', 'name', 'date_of_birth', 'is_staff')
