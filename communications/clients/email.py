from typing import List

from django.conf import settings
from django.core.mail import send_mail
from structlog import get_logger

log = get_logger(__name__)


class BaseEmailClient:
    def send_email(
        self, subject: str, message: str, receiver_list: List[str], from_email: str
    ) -> bool:
        raise NotImplementedError()


class DjangoEmailClient(BaseEmailClient):
    def send_email(
        self,
        subject: str,
        message: str,
        recipient_list: List[str],
        from_email: str = settings.EMAIL_HOST_USER,
    ) -> bool:
        try:
            send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False,
            )
            return True
        except Exception as e:
            log.error(
                "Email send error.",
                subject=subject,
                from_email=from_email,
                recepient_list=recipient_list,
                exception=e,
            )
            raise e


def get_email_service() -> BaseEmailClient:
    return DjangoEmailClient()
