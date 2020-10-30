from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    """
    BearerTokenAuthentication authenticats a rest api request based on Bearer token
    """

    keyword = 'Bearer'
