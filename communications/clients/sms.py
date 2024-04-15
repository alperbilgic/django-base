import httpx
from django.conf import settings
from structlog import get_logger

log = get_logger(__name__)


class BaseSMSClient:
    def send_sms(self, receiver, language, message, header) -> bool:
        raise NotImplementedError()


class NetgsmSMSClient(BaseSMSClient):
    def is_netgsm_error_code(self, text):
        if text in ["20", "30", "40", "50", "51", "70", "85"]:
            return True
        return False

    def send_sms(self, receiver: str, language: str, message: str, header: str) -> bool:
        query_params = {
            "usercode": settings.NETGSM_USER_CODE,
            "password": settings.NETGSM_PASSWORD,
            "gsmno": receiver,
            "message": message,
            "msgheader": header,
        }

        response = httpx.get(
            "https://api.netgsm.com.tr/sms/send/get/", params=query_params
        )
        success = not self.is_netgsm_error_code(response.text)
        log.info(
            "SMS message has been sent.",
            gsmno=receiver,
            message=message,
            msgheader=header,
            dil=language,
            success=success,
            response_text=response.text,
            response_status_code=response.status_code,
        )
        return success


def get_sms_client() -> BaseSMSClient:
    return NetgsmSMSClient()
