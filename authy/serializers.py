from typing import Dict, Union

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, Token

from authy.helpers.token_helper import (
    get_token_subscription_for_user,
    set_token_parameters,
)
from common.custom_exceptions.custom_exception import CustomException
from common.response.response_information_codes.error_code import ErrorCode
from subscription.models import UserSubscription
from user.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    @classmethod
    def get_token(cls, account, user):
        token = super().get_token(account)

        token["email"] = user.email
        token["phone"] = user.phone and user.phone.as_international.replace(" ", "")
        token["user_id"] = str(user.id)
        token["role"] = user.role
        token["school_id"] = str(user.school_id) if user.school_id else None

        return token


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(
        max_length=254, allow_null=True, allow_blank=True, required=False
    )
    phone = PhoneNumberField(required=False, allow_null=True, allow_blank=True)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data.get("email", None)
        phone = data.get("phone", None)

        if email:
            email = email.strip().lower()

        if not email and not phone:
            raise CustomException(
                detail={
                    "email": "Cannot be empty if no phone provided",
                    "phone": "Cannot be empty if no email provided",
                },
                code=ErrorCode.GENERAL_VALIDATION_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST,
                message=_("Email or phone should be provided"),
            )

        if email and phone:
            raise CustomException(
                detail={
                    "email": "Should not be provided if phone provided",
                    "phone": "Should not be provided if email provided",
                },
                code=ErrorCode.GENERAL_VALIDATION_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST,
                message=_("Enter email or phone not both"),
            )

        password = data["password"]
        user = (
            User.objects.filter(email=email).select_related("locale").first()
            if email
            else User.objects.filter(phone=phone).select_related("locale").first()
        )

        if user is None:
            raise CustomException(
                detail={"email": ["User with this email doesn't exist"]},
                code=ErrorCode.NOT_FOUND_ERROR,
                status_code=status.HTTP_404_NOT_FOUND,
                message=(
                    _("User with this email doesn't exist")
                    if email
                    else _("User with this phone doesn't exist")
                ),
            )
        account = authenticate(id=user.account_id, password=password)

        if account is None:
            raise CustomException(
                detail={
                    "email": ["Invalid email or password"],
                    "password": ["Invalid email or password"],
                },
                code=ErrorCode.AUTHENTICATION_FAILED,
                status_code=status.HTTP_400_BAD_REQUEST,
                message=_("Incorrect password"),
            )

        try:
            token = CustomTokenObtainPairSerializer.get_token(account, user)
            refresh_token = token
            access_token = token.access_token
            subscription = get_token_subscription_for_user(user)
            access_token = set_token_parameters(
                access_token,
                {
                    "subscription": (
                        subscription.safe_json() if subscription is not None else None
                    ),
                    "locale_code": user.locale.code,
                },
            )

            update_last_login(None, account)

            validation = {
                "access": str(access_token),
                "refresh": str(refresh_token),
                "user": user.to_dict(),
            }
            return validation
        except ObjectDoesNotExist:
            raise CustomException(
                "Invalid login credentials",
                ErrorCode.AUTHENTICATION_FAILED,
                status.HTTP_400_BAD_REQUEST,
                message=_("Invalid login credentials"),
            )


class UserRegisterSerializer(serializers.Serializer):
    phone = PhoneNumberField(allow_null=True, allow_blank=True, required=False)
    email = serializers.CharField(
        max_length=254, required=False, allow_blank=True, allow_null=True
    )
    password = serializers.CharField(max_length=128, write_only=True, required=True)
    verify_password = serializers.CharField(
        max_length=128, write_only=True, required=True
    )

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data.get("email", None)
        phone = data.get("phone", None)
        password = data.get("password")
        verify_password = data.get("verify_password")

        if not email and not phone:
            raise CustomException(
                detail={
                    "error": {
                        "email": "Cannot be null or empty if no phone provided",
                        "phone": "Cannot be null or empty if no email provided",
                    }
                },
                code=ErrorCode.GENERAL_VALIDATION_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST,
                message=_("Email or phone should be provided"),
            )

        if not password == verify_password:
            raise CustomException(
                detail={"verify_password": ["Password doesn't match"]},
                code=ErrorCode.PASSWORD_DOES_NOT_MATCH,
                status_code=status.HTTP_400_BAD_REQUEST,
                message=_("Passwords doesn't match"),
            )

        validation = {
            "phone": data.get("phone") if data.get("phone") else None,
            "email": data.get("email").lower().strip() if data.get("email") else None,
            "password": data.get("password"),
        }

        return validation


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=True, allow_blank=True, required=False)
    phone = serializers.CharField(allow_null=True, allow_blank=True, required=False)


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")
        request = self.context.get("request", None)
        if request is None:
            raise CustomException.from_exception(
                Exception("Request could not be gotten"),
                code=ErrorCode.INTERNAL_SERVER_ERROR,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        account = request.user if request else None

        account = authenticate(id=account.id, password=old_password)
        errors = {}
        if not account:
            errors.update({"old_password": ["Password is incorrect!"]})

        if new_password != confirm_password:
            errors.update({"confirm_password": ["Given passwords doesn't match"]})

        if errors:
            raise CustomException(
                detail=errors,
                code=ErrorCode.GENERAL_VALIDATION_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        account.set_password(new_password)
        account.save()
        return {}


class CustomTokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)
    token_class = RefreshToken

    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])
        access_token = refresh.access_token
        subscription = self.get_user_subscription_from_token(access_token)
        access_token = self.set_token_parameters(
            access_token,
            {
                "subscription": (
                    subscription.safe_json() if subscription is not None else None
                ),
                "locale_code": access_token.payload.get("locale_code"),
            },
        )

        data = {"access": str(access_token)}

        if settings.SIMPLE_JWT["ROTATE_REFRESH_TOKENS"]:
            if settings.SIMPLE_JWT["BLACKLIST_AFTER_ROTATION"]:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh"] = str(refresh)

        return data

    def set_token_parameters(self, token: Token, parameters: Dict[str, any]) -> Token:
        for key in parameters.keys():
            token.payload[key] = parameters[key]

        return token

    def get_user_subscription_from_token(
        self, token: Token
    ) -> Union[UserSubscription, None]:
        payload = token.payload
        user_id = payload.get("user_id", None)
        if user_id is not None:
            user = User.objects.get(pk=user_id)
            return get_token_subscription_for_user(user)

        else:
            return None
