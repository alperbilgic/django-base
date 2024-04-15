from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework import status

from common.custom_exceptions.custom_exception import CustomException
from common.response.response_information_codes.error_code import ErrorCode


class CustomUserManager(BaseUserManager):
    """
    Custom user model where the email address is the unique identifier
    and has an is_admin field to allow access to the admin app
    """

    def create_user_with_default_password(self, password, **extra_fields):
        if not password:
            password = settings.DEFAULT_USER_KEY
        return self._create_user(password, **extra_fields)

    def create_user_with_password(self, password, **extra_fields):
        if not password:
            raise CustomException.from_exception(
                ValueError(_("The password must be set")),
                ErrorCode.PASSWORD_NOT_PROVIDED,
                message=_("The password must be set"),
            )
        return self._create_user(password, **extra_fields)

    def _create_user(self, password, **extra_fields):
        user = self.model(**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_admin(self, password, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", 5)

        if extra_fields.get("role") != 5:
            raise CustomException.from_exception(
                ValueError("Superuser must have role of Global Admin"),
                ErrorCode.GENERAL_VALIDATION_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        return self.create_user_with_password(password, **extra_fields)
