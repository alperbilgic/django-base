import threading
from typing import TYPE_CHECKING
from typing import Union

from django.utils.functional import cached_property
from pytz.tzinfo import DstTzInfo, StaticTzInfo
from rest_framework.request import Request
from rest_framework.response import Response

from user.types import UserRole
from utils.date import timezone_with_fallback

if TYPE_CHECKING:
    from user.models import User


class GlobalContext:
    def __init__(self, request: Request):
        self.request = request

    @cached_property
    def user_id(self) -> int:
        return (
            self.request.auth.payload.get("user_id")
            if self.request.auth and self.request.auth.payload
            else None
        )

    @cached_property
    def user_role(self) -> UserRole:
        return (
            UserRole(self.request.auth.payload.get("role", UserRole.NONE.value))
            if self.request.auth and self.request.auth.payload
            else UserRole.NONE
        )

    @cached_property
    def user_school_id(self) -> str:
        return (
            self.request.auth.payload.get("school_id", None)
            if self.request.auth and self.request.auth.payload
            else None
        )

    @cached_property
    def user_timezone(self) -> Union[StaticTzInfo, DstTzInfo]:
        timezone_header = self.request.META.get("HTTP_USER_TIMEZONE", "UTC")
        return timezone_with_fallback(timezone_header)

    @cached_property
    def user(self) -> Union["User", None]:
        account = self.request.user
        if str(account.__class__.__name__) == "Account":
            return account.user
        return None

    @cached_property
    def language_code(self) -> str:
        """
        Returns selected language code
        If language or locale fields are provided in query_params set to that value
        Else if user is logged in return user locale_code
        """
        language_code = (
            self.request.META.get("HTTP_ACCEPT_LANGUAGE")
            or self.request.GET.get("language", None)
            or self.request.GET.get("locale_code", None)
        )
        if language_code:
            return language_code

        token_language_code = (
            self.request.auth.payload.get("locale_code", None)
            if self.request.auth and self.request.auth.payload
            else None
        )
        return token_language_code or "tr"


class GlobalContextMiddleware:
    """
    Provides storage for the "current" request object, so that code anywhere
    in your project can access it, without it having to be passed to that code
    from the view.
    """

    _contexts = {}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Request):
        self.process_request(request)
        response = self.get_response(request)
        self.process_response(request, response)
        return response

    def process_request(self, request: Request):
        """
        Store the current request.
        """
        global_context = GlobalContext(request)
        self.__class__.set_global_context(global_context)

    def process_response(self, request: Request, response: Response):
        """
        Delete the current request to avoid leaking memory.
        """
        self.__class__.del_global_context()
        return response

    @classmethod
    def get_global_context(cls, default=None) -> GlobalContext:
        """
        Retrieve the request object for the current thread, or the optionally
        provided default if there is no current request.
        """
        return cls._contexts.get(threading.current_thread(), default)

    @classmethod
    def set_global_context(cls, context: GlobalContext) -> None:
        """
        Save the given request into storage for the current thread.
        """
        cls._contexts[threading.current_thread()] = context

    @classmethod
    def del_global_context(cls) -> None:
        """
        Delete the request that was stored for the current thread.
        """
        cls._contexts.pop(threading.current_thread(), None)
