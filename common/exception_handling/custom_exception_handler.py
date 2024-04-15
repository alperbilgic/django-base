from django.conf import settings
from rest_framework.exceptions import APIException
from structlog import get_logger

from common.custom_exceptions.custom_exception import CustomException
from common.exception_handling.exception_handler_mapper import (
    EXCEPTION_HANDLER_MAPPER,
    API_EXCEPTION_HANDLER_MAPPER,
)
from common.response.view_response import ViewFailResponse, log_view_response

log = get_logger(__name__)


def custom_exception_handler(exc, context):
    if isinstance(exc, CustomException):
        view_response = ViewFailResponse(
            exception=exc,
            error_msg=exc.detail,
            response_status=exc.status_code,
            response_information_code=exc.code,
            response_message=exc.message,
        )
    elif isinstance(exc, APIException):
        view_response = ViewFailResponse(
            exception=exc,
            error_msg=exc.detail,
            response_status=exc.status_code,
            **vars(
                API_EXCEPTION_HANDLER_MAPPER.get(
                    exc.__class__, API_EXCEPTION_HANDLER_MAPPER.get(APIException)
                )
            )
        )
    else:
        exception_handling_parameters = EXCEPTION_HANDLER_MAPPER.get(
            exc.__class__, EXCEPTION_HANDLER_MAPPER.get(Exception)
        )(exc)
        if settings.DEBUG:
            exception_handling_parameters.error_msg += " Exception: " + str(exc)
        view_response = ViewFailResponse(
            exception=exc, **vars(exception_handling_parameters)
        )

    view_class = (
        context.get("view").__class__.__name__
        if context.get("view", None) is not None
        else None
    )
    request_data = (
        context.get("request").data
        if context.get("request", None) is not None
        else None
    )
    path = (
        context.get("request").get_full_path()
        if context.get("request", None) is not None
        else None
    )
    request_method = (
        context.get("request").method
        if context.get("request", None) is not None
        else None
    )

    log_view_response(
        struct_logger=log,
        view_name=view_class,
        method_name="",
        request_body=request_data,
        request_path=path,
        request_method=request_method,
        view_response=view_response,
    )
    return view_response.rest_response
