from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details

from common.response.response_information_codes.error_code import ErrorCode


class CustomException(APIException):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _("A server error occurred.")
    default_code = ErrorCode.INTERNAL_SERVER_ERROR
    default_message = _("A server error occurred.")

    def __init__(self, detail=None, code=None, status_code=None, message=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        if message is None:
            message = self.default_message

        self.code = code
        self.message = message
        self.detail = _get_error_details(detail, code)
        if status_code is not None:
            self.status_code = status_code

    def __str__(self):
        return str(self.detail)

    @classmethod
    def from_exception(
        cls, exc: Exception, code=None, status_code=None, message: str = None
    ):
        detail = str(exc)
        return cls(detail, code, status_code, message)
