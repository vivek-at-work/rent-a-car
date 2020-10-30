from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

PRESENT_OR_FUTURE = 'CURRENT_OR_FUTURE'
PRESENT_OR_PAST = 'PRESENT_OR_PAST'


def date_validator(date_type, current_time=timezone.now()):
    if date_type not in [PRESENT_OR_FUTURE, PRESENT_OR_PAST]:
        raise Exception(message='Not a valid date_type choice.')

    def validator(value):
        if date_type == PRESENT_OR_FUTURE and current_time > value:
            raise ValidationError(
                _('%(value)s is not a valid value.'),
                params={'value': value},
            )

        if date_type == PRESENT_OR_PAST and current_time < value:
            raise ValidationError(
                _('%(value)s is not a valid value.'),
                params={'value': value},
            )

    return validator
