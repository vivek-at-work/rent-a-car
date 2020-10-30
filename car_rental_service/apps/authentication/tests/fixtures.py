from datetime import date

from django.utils import timezone

NAME = 'VIVEK SRIVASTAVA'
TODAY = timezone.localdate()
VALID_DOB = date(TODAY.year-20, TODAY.month, TODAY.day)
CONTACT_NUMBER = '9657946755'
PASSWORD = 'Qwerty@1234'
VALID_USER_DATA = {
    'name':NAME,
    'date_of_birth':VALID_DOB,
    'contact_number':CONTACT_NUMBER,
    'password':PASSWORD
}
