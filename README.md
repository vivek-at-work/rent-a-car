# Car Rental Service

Car Rental Service carries the capability for renting cars, track their booking histories and monitor availability for next bookings.

### CODE STRUCTURE

We have divided our codebase into multiple smaller apps to avoid a monolithic design to increase readability and flexibility to experiment within the code.

#### car_rental_service

1.  This package carries our settings and URLs.
2.  It is generated using Django-admin command and it is recommended to keep it as light as possible which keeps our codebase to more readable and loosely coupled

#### apps:

apps directory works as a parent or container of all other sub-apps listed bellow.

1.  authentication - This app takes care of user authentication based on contact number and password along with that it defines the structure of our token-based authentication.

2.  bookings: - bookings app is created to record bookings done by a customer - bookings app provides us with the endpoints to close an existing booking and list down the bookings done previously

3.  customers - Customers app is created for managing user data so that if the user does the second booking we will be able to reuse his existing data and can avoid redundancy.it replaces Django's default user definition so that we can enable our customers to register with our car rental service

4.  calculators: calculators app is responsible for calculation of payable amount for a booking based on the car type it enables us with a plug and plays modal for calculations

5.  catalogue: catalogue app provides us with an endpoint to list cars available for bookings, rent a car or to register a new car to the service

## OUR TECH STACK:

- **python** : As of now we are using python 3.6.
- **pipenv** : For our dependency management.
- **Django** : As our core web framework.
- **Django Rest Framework**: To help us with rest API development.

For other python packages please refer Pipfile available with the codebase

## SETTINGS TO CONSIDER

```
SECRET_KEY = os.environ.get('CRS_SECRET_KEY',
'bup+h4vd-dy)0!kv(8kqjwbz-(h^bx19@^jd^2zc#$zyp\*o0$o')

AUTH_USER_MODEL = 'customers.Customer'

AUTHENTICATION_BACKENDS = [
'django.contrib.auth.backends.ModelBackend',
'authentication.backends.ConatctNumberBasedAuthenticationsBackend
]

REST_FRAMEWORK = {
'DEFAULT_AUTHENTICATION_CLASSES': [
'authentication.bearer_token.BearerTokenAuthentication',
],
'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema'
}
SPECTACULAR_SETTINGS = {
'TITLE': 'Car Rental Service',
'DESCRIPTION': "Car Rental Service enables us with renting a car and track it's booking history and monitor its availability for next bookings.",
'VERSION': '1.0.0'
}

BASE_DAY_RENTAL = os.environ.get('CRS_BASE_DAY_RENTAL',10)

PER_KILOMETER_PRICE = os.environ.get('CRS_PER_KILOMETER_PRICE', 2)
```

## ASSUMPTIONS / FEATURES

1.  Customer Has to signup before booking using contact number name date of birth and password.
2.  Once Logged In User can request for available Cars
3.  Users can select a car and can provide its booking start date.
4.  User can close his booking by providing closing time and last milage of the car and once he closes that booking he will be displayed the total payable amount for that particular booking.

## OUR CI WORKFLOW

    Follow this link to how our last commit worked
    https://github.com/vivek-at-work/rent-a-car/actions

## DEV SETUP

    ### Prerequisites : Linux , pipenv
    1. git clone https://github.com/vivek-at-work/rent-a-car.git
    2. cd rent-a-car/
    3. pipenv install
    4. pipenv shell
    5. cd car_rental_service
    6. python manage.py migrate
    7. python manage.py runserver 8001

## REST API DOCUMENTATION

    Follow this link to know about our rest apis
     http://localhost:8001/api/schema/swagger-ui/#/
![Our API Docs](our_api_doc.JPG?raw=true "We Use Swagger")
