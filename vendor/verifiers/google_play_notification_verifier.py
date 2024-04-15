import base64
import json
from datetime import datetime

from vendor.types import (
    StoreNotificationVerificationResult,
    GooglePlayNotificationType,
    GooglePlayNotificationSubtype,
)


class InvalidTokenError(Exception):
    pass


class GooglePlayNotificationVerifier:
    @staticmethod
    def parse(request_body) -> StoreNotificationVerificationResult:
        message = request_body.get("message")
        data = json.loads(base64.b64decode(message.get("data", "")))
        notification_id = message.get("messageId")
        publish_time = datetime.strptime(
            message.get("publishTime"), "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        (
            notification_type,
            subtype_num,
        ) = GooglePlayNotificationType.get_type_from_notification_data(data)
        subtype = GooglePlayNotificationSubtype(subtype_num)
        return StoreNotificationVerificationResult.from_verification_result(
            notification_type=notification_type,
            subtype=subtype,
            notification_id=notification_id,
            data=data,
            notification_publish_time=publish_time,
        )
