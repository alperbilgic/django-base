from typing import Dict

from rest_framework_simplejwt.tokens import Token

from user.models import User


def get_token_subscription_for_user(user: User):
    subscription = user.last_or_active_subscription
    return subscription


def set_token_parameters(token: Token, parameters: Dict[str, any]) -> Token:
    for key in parameters.keys():
        token.payload[key] = parameters[key]

    return token
