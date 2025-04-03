from rest_framework import status
from rest_framework.exceptions import APIException


class FeeException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class RoutingException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class IrregularWalletException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
