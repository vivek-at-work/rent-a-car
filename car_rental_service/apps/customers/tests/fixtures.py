from datetime import date

from customers.models import Customer

CUSTOMER = Customer
NAME = 'VIVEK SRIVASTAVA'
TODAY = date.today()
INVALID_DOB = TODAY
VALID_DOB = date(TODAY.year - 20, TODAY.month, TODAY.day)
CONTACT_NUMBER = '9657946755'
INVALID_CONTACT_NUMBER = '1657946751'
PASSWORD = 'Qwerty@1234'
