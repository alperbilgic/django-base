from payment.subscription.strategies import (
    GooglePurchaseStrategy,
    ApplePurchaseStrategy,
)
from payment.types import PaymentVendor

SUBSCRIPTION_STRATEGY_MAPPER = {
    PaymentVendor.FREE: None,
    PaymentVendor.GOOGLE: GooglePurchaseStrategy,
    PaymentVendor.APPLE: ApplePurchaseStrategy,
}
