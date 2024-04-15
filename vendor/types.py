from datetime import datetime
from enum import Enum, auto
from typing import Dict, Union

from utils.custom_types.dict_extender import BaseDictExtender


class GooglePlayNotificationType(Enum):
    NONE = auto()
    SUBSCRIPTION_NOTIFICATION = auto()
    ONE_TIME_PRODUCT_NOTIFICATION = auto()
    TEST_NOTIFICATION = auto()

    @classmethod
    def get_type_from_notification_data(
        cls, data: Dict
    ) -> (Union[None, "GooglePlayNotificationType"], int):
        if "oneTimeProductNotification" in data:
            return cls.ONE_TIME_PRODUCT_NOTIFICATION, data.get(
                "oneTimeProductNotification"
            ).get("notificationType")
        if "subscriptionNotification" in data:
            return cls.SUBSCRIPTION_NOTIFICATION, data.get(
                "subscriptionNotification"
            ).get("notificationType")
        if "testNotification" in data:
            return cls.TEST_NOTIFICATION, data.get("testNotification").get(
                "notificationType"
            )
        return None

    @classmethod
    def _missing_(cls, value):
        return cls.NONE

    def __hash__(self):
        return self.value


class GooglePlayNotificationSubtype(Enum):
    NONE = 0
    SUBSCRIPTION_RECOVERED = 1
    SUBSCRIPTION_RENEWED = 2
    SUBSCRIPTION_CANCELED = 3
    SUBSCRIPTION_PURCHASED = 4
    SUBSCRIPTION_ON_HOLD = 5
    SUBSCRIPTION_IN_GRACE_PERIOD = 6
    SUBSCRIPTION_RESTARTED = 7
    SUBSCRIPTION_PRICE_CHANGE_CONFIRMED = 8
    SUBSCRIPTION_DEFERRED = 9
    SUBSCRIPTION_PAUSED = 10
    SUBSCRIPTION_PAUSE_SCHEDULE_CHANGED = 11
    SUBSCRIPTION_REVOKED = 12
    SUBSCRIPTION_EXPIRED = 13

    @classmethod
    def _missing_(cls, value):
        return cls.NONE

    def __hash__(self):
        return self.value


class AppStoreNotificationType(Enum):
    NONE = "NONE"
    CONSUMPTION_REQUEST = "CONSUMPTION_REQUEST"
    DID_CHANGE_RENEWAL_PREF = "DID_CHANGE_RENEWAL_PREF"
    DID_CHANGE_RENEWAL_STATUS = "DID_CHANGE_RENEWAL_STATUS"
    DID_FAIL_TO_RENEW = "DID_FAIL_TO_RENEW"
    DID_RENEW = "DID_RENEW"
    EXPIRED = "EXPIRED"
    GRACE_PERIOD_EXPIRED = "GRACE_PERIOD_EXPIRED"
    OFFER_REDEEMED = "OFFER_REDEEMED"
    PRICE_INCREASE = "PRICE_INCREASE"
    REFUND = "REFUND"
    REFUND_DECLINED = "REFUND_DECLINED"
    REFUND_REVERSED = "REFUND_REVERSED"
    RENEWAL_EXTENDED = "RENEWAL_EXTENDED"
    RENEWAL_EXTENSION = "RENEWAL_EXTENSION"
    REVOKE = "REVOKE"
    SUBSCRIBED = "SUBSCRIBED"
    TEST = "TEST"

    @classmethod
    def _missing_(cls, value):
        return cls.NONE

    def __hash__(self):
        return hash(self.value)


class AppStoreNotificationSubtype(Enum):
    NONE = "NONE"
    UPGRADE = "UPGRADE"
    DOWNGRADE = "DOWNGRADE"
    AUTO_RENEW_ENABLED = "AUTO_RENEW_ENABLED"
    AUTO_RENEW_DISABLED = "AUTO_RENEW_DISABLED"
    INITIAL_BUY = "INITIAL_BUY"
    RESUBSCRIBE = "RESUBSCRIBE"
    OFFER_REDEEMED = "OFFER_REDEEMED"
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    SUMMARY = "SUMMARY"
    FAILURE = "FAILURE"

    @classmethod
    def _missing_(cls, value):
        return cls.NONE

    def __hash__(self):
        return hash(self.value)


class StoreNotificationVerificationResult(BaseDictExtender):
    def __init__(
        self,
        notification_type: Enum,
        subtype: Enum,
        notification_id: str,
        data: Dict,
        notification_publish_time: datetime,
    ):
        self.notification_type = notification_type
        self.subtype = subtype
        self.notification_id = notification_id
        self.data = data
        self.notification_publish_time = notification_publish_time

    @classmethod
    def from_verification_result(
        cls,
        notification_type: Enum,
        subtype: Enum,
        notification_id: str,
        data: Dict,
        notification_publish_time: datetime,
    ):
        """
        :param notification_type: Notification type (GoogleNotificationType, AppleNotificationType)
        :param subtype: Notification subtype (GoogleNotificationTypeSubtype, AppleNotificationSubtype)
        :param notification_id: Unique string parameter provided by vendor
        :param data: Dict data provided by the vendor
        :param notification_publish_time: Publish time of the notification
        """
        return cls(
            notification_type=notification_type,
            subtype=subtype,
            notification_id=notification_id,
            data=data,
            notification_publish_time=notification_publish_time,
        )
