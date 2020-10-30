import re
from datetime import date

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_contact_number(value):
    if not re.match(r'[789]\d{9}$', value):
        raise ValidationError(
            _('%(value)s is not a valid contact number'), params={'value': value},
        )


def validate_date_of_birth(value):
    # TODO:  make it timezone aware
    today = date.today()
    birthday = value.replace(year=today.year)
    if birthday > today or today.year - value.year < 18:
        raise ValidationError(
            _('%(value)s is not a valid date of birth'), params={'value': value},
        )
