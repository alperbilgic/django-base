from vendor.strategies.google_subscription_notification_strategy import (
    GoogleSubscriptionNotificationStrategy,
    AppleSubscriptionNotificationStrategy,
)


GOOGLE_NOTIFICATION_STRATEGY_MAP = {
    "subscription": GoogleSubscriptionNotificationStrategy
}

APPLE_NOTIFICATION_STRATEGY_MAP = {
    "subscription": AppleSubscriptionNotificationStrategy
}
