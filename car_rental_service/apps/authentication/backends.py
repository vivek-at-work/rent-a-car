import logging

from django.contrib.auth import backends, get_user_model

USER = get_user_model()
logger = logging.getLogger(__name__)


class ConatctNumberBasedAuthenticationsBackend(backends.ModelBackend):
    """
    Authenticate users based on contact number instead of username.
    We need this as we are providing the functionality to use contact number
    as username to login to our car rental service.
    """

    def authenticate(self, request, **kwargs):
        contact_number = kwargs.get('contact_number', None)
        password = kwargs.get('password', None)
        if not contact_number:
            # django admin login still sends username
            contact_number = kwargs.get('username', None)
        if None in [contact_number, password]:
            logger.error('Invalid Request received for login.')
            return None
        try:
            user = USER.objects.get(contact_number=contact_number)
            if user.check_password(password) is True:
                logger.info('User %s logged in to the car rental service', user)
                return user
            logger.info(
                'Password check failed for User %s while logging  in to the car rental service.',
                user,
            )
            return None
        except USER.DoesNotExist:
            logger.warning(
                'Someone tried to use %s to logging  in to the car rental service and failed',
                contact_number,
            )
            return None
