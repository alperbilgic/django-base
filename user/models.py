import uuid
from datetime import datetime
from typing import List, Dict

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q, Case, When, Value, CharField
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django_softdelete.models import SoftDeleteModel
from phonenumber_field.modelfields import PhoneNumberField

from authy.models import Account
from subscription.models import UserSubscription
from subscription.types import SubscriptionStatus
from user.types import UserRole
from utils.converters import ModelConverter
from utils.fields import DateTimeWithoutTZField


class Locale(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False, unique=True)
    code = models.CharField(
        max_length=16, blank=False, null=False, unique=True, default="tr"
    )
    created = DateTimeWithoutTZField(auto_now_add=True, editable=False, null=True)
    updated = DateTimeWithoutTZField(auto_now=True, editable=False, null=True)

    class Meta:
        db_table = "locale"

    @classmethod
    def get_default(cls) -> "Locale":
        locale, created = cls.objects.get_or_create(
            name="Turkey",
            code="tr",
        )
        return locale

    @classmethod
    def get_default_id(cls) -> "Locale":
        locale, created = cls.objects.get_or_create(
            name="Turkey",
            code="tr",
        )
        return locale.id

    @classmethod
    def get_default_english(cls) -> "Locale":
        locale, created = cls.objects.get_or_create(
            name="England",
            code="en",
        )
        return locale


class User(SoftDeleteModel):
    username_validator = UnicodeUsernameValidator()

    PERSONAL = "PERSONAL"
    BUSINESS = "BUSINESS"
    INTERNAL = "INTERNAL"
    CREATION_TYPE = [
        (PERSONAL, _("Personal")),
        (BUSINESS, _("Business")),
        (INTERNAL, _("Internal")),
    ]

    id = models.UUIDField(
        unique=True, primary_key=True, default=uuid.uuid4, editable=False
    )
    phone = PhoneNumberField(null=True, blank=True)
    phone_verified = models.BooleanField(null=False, blank=False, default=False)
    email = models.EmailField(null=True, blank=True)
    email_verified = models.BooleanField(null=False, blank=False, default=False)
    fullname = models.CharField(max_length=255, blank=True)
    role = models.CharField(
        max_length=64, choices=UserRole.choices, default=UserRole.STUDENT.value
    )
    student_class = models.ForeignKey(
        "user.Class",
        on_delete=models.SET_NULL,
        db_column="class_id",
        related_name="users",
        null=True,
    )
    school = models.ForeignKey(
        "user.School", on_delete=models.SET_NULL, related_name="users", null=True
    )
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name="user", null=False
    )
    locale = models.ForeignKey(
        Locale,
        on_delete=models.CASCADE,
        related_name="users",
        default=Locale.get_default_id,
    )
    creation_type = models.CharField(
        max_length=16, choices=CREATION_TYPE, null=False, blank=False
    )
    avatar = models.ForeignKey(
        "user.Avatar",
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
    )
    created = DateTimeWithoutTZField(auto_now_add=True, editable=False)
    updated = DateTimeWithoutTZField(auto_now=True, editable=False)
    deleted_at = DateTimeWithoutTZField(blank=True, null=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"
        constraints = [
            models.UniqueConstraint(
                fields=["phone"],
                condition=Q(deleted_at__isnull=True)
                & Q(phone__isnull=False)
                & ~Q(phone=""),
                name="user_unique_phone",
            ),
            models.UniqueConstraint(
                fields=["email"],
                condition=Q(deleted_at__isnull=True)
                & Q(email__isnull=False)
                & ~Q(email=""),
                name="user_unique_email",
            ),
            models.CheckConstraint(
                check=(Q(email__isnull=False) & ~Q(email__exact=""))
                | (Q(phone__isnull=False) & ~Q(phone__exact="")),
                name="user_at_least_email_or_phone_not_null",
            ),
        ]
        indexes = [models.Index(fields=["created"])]

    @property
    def phone_as_international(self):
        return self.phone.as_international if self.phone else None

    @cached_property
    def active_subscription(self) -> UserSubscription:
        active_statuses = filter(
            lambda choice: choice.is_active, [choice for choice in SubscriptionStatus]
        )
        return (
            self.subscriptions.filter(status__in=active_statuses)
            .order_by("-id")
            .first()
        )

    @cached_property
    def last_or_active_subscription(self) -> UserSubscription:
        subscriptions = (
            self.subscriptions.select_related("buyable")
            .annotate(
                priority=Case(
                    When(status="active", then=Value(1)),
                    default=Value(2),
                    output_field=CharField(),
                )
            )
            .order_by("priority", "-created")
        )

        return subscriptions.first()

    @property
    def has_active_subscription(self):
        return self.active_subscription is not None

    def to_dict(
        self,
        fields: List = None,
        exclude: List = None,
        detailed_fields: Dict = None,
        fields_as: Dict = None,
    ):
        user_dict = ModelConverter.model_to_dict(
            self,
            fields=fields,
            exclude=exclude,
            detailed_fields=detailed_fields,
            fields_as=fields_as,
        )

        if user_dict.get("phone"):
            user_dict["phone"] = user_dict["phone"].as_international.replace(" ", "")
        return user_dict


class Avatar(models.Model):
    image = models.CharField(max_length=2048, blank=False, null=True)
    created = DateTimeWithoutTZField(auto_now_add=True, editable=False)
    updated = DateTimeWithoutTZField(auto_now=True, editable=False)

    class Meta:
        db_table = "avatar"


class Class(models.Model):
    id = models.UUIDField(
        unique=True, primary_key=True, default=uuid.uuid4, editable=False
    )
    branch = models.CharField(max_length=64, blank=False, null=False)
    school = models.ForeignKey(
        "user.School", null=False, related_name="classes", on_delete=models.CASCADE
    )
    created = DateTimeWithoutTZField(auto_now_add=True, editable=False)
    updated = DateTimeWithoutTZField(auto_now=True, editable=False)

    class Meta:
        unique_together = ("branch", "school")
        db_table = "class"


class School(models.Model):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    ROLE = [
        (PUBLIC, _("Public")),
        (PRIVATE, _("Private")),
    ]

    id = models.UUIDField(
        unique=True, primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.ForeignKey(
        "common.Translation",
        on_delete=models.CASCADE,
        related_name="named_schools",
        null=False,
    )
    type = models.CharField(max_length=15, choices=ROLE, default=PUBLIC)
    created = DateTimeWithoutTZField(auto_now_add=True, editable=False)
    updated = DateTimeWithoutTZField(auto_now=True, editable=False)

    class Meta:
        db_table = "school"
