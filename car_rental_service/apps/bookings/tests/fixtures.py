from datetime import date, timedelta

from django.utils import timezone

NOW = timezone.now()
FUTURE = NOW + timedelta(hours=2)
PAST = NOW - timedelta(hours=2)
today = timezone.localdate()
VALID_DOB = date(today.year - 20, today.month, today.day)

CAR_DATA = {'number': 'PRE1', 'category': 2, 'current_milage': 12.0}
CAR_DATA_PREMIUM = {'number': 'PRE1', 'category': 1, 'current_milage': 12.0}
CAR_DATA_MINI = {'number': 'PRE1', 'category': 3, 'current_milage': 12.0}
CUSTOMER_DATA = {
    'contact_number': '9657946755',
    'name': 'Vivek Srivastava',
    'date_of_birth': VALID_DOB,
    'password': 'Qwerty@1234',
}
CUSTOMER_DATA_TWO = {
    'contact_number': '9888888851',
    'name': 'Vivek Srivastava',
    'date_of_birth': VALID_DOB,
    'password': 'Qwerty@1234',
}
