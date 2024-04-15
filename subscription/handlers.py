import datetime

from dateutil.relativedelta import relativedelta
from django.dispatch import receiver
from structlog import get_logger

from payment.signals import purchase_for_subscription_created
from payment.types import BuyableType, SubscriptionPeriod
from subscription.models import UserSubscription
from subscription.types import SubscriptionStatus

log = get_logger(__name__)


@receiver(purchase_for_subscription_created, sender=None)
def handle_user_subscription_create(sender, instance, product=None, **kwargs):
    # Create user subscription
    purchase = instance.purchase
    if not product:
        subscription_product = purchase.buyables.filter(
            type__in=[BuyableType.PERSONAL_SUBSCRIPTION]
        ).first()
    else:
        subscription_product = product
    if not subscription_product:
        return

    user = purchase.user

    if user.has_active_subscription:
        if user.active_subscription.purchase.id == purchase.id:
            user.active_subscription.renew(from_now=False)
        return

    current_time = datetime.datetime.utcnow()
    no_trial = (
        subscription_product.trial_days is None or subscription_product.trial_days == 0
    )

    UserSubscription.objects.create(
        user=user,
        buyable=subscription_product,
        purchase=purchase,
        expiration_date=(
            current_time
            + UserSubscription.time_to_add_after_expiration(
                SubscriptionPeriod(subscription_product.period)
            )
            if no_trial
            else current_time + relativedelta(days=subscription_product.trial_days)
        ),
        start_date=current_time,
        status=SubscriptionStatus.ACTIVE if no_trial else SubscriptionStatus.TRIAL,
        used_trial_days=subscription_product.trial_days,
    )
