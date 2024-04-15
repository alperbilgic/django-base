from django.db import models


class SubscriptionStatus(models.TextChoices):
    INITIAL = "initial"
    TRIAL = "trial"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CANCELED = "canceled"
    EXPIRED = "expired"

    @staticmethod
    def is_active_value(status: str):
        ACTIVE_STATUSES = [
            SubscriptionStatus.TRIAL,
            SubscriptionStatus.ACTIVE,
            SubscriptionStatus.CANCELED,
        ]

        return SubscriptionStatus(status) in ACTIVE_STATUSES

    @property
    def is_active(self):
        return SubscriptionStatus.is_active_value(self.value)
