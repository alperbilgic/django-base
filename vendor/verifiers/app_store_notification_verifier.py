import datetime
import os

import jwt
from OpenSSL.crypto import (
    X509StoreContextError,
    load_certificate,
    FILETYPE_ASN1,
)

from vendor.types import (
    StoreNotificationVerificationResult,
    AppStoreNotificationSubtype,
    AppStoreNotificationType,
)


class InvalidTokenError(Exception):
    pass


class AppStoreNotificationVerifier:
    @staticmethod
    def add_labels(key: str) -> bytes:
        return (
            "-----BEGIN CERTIFICATE-----\n" + key + "\n-----END CERTIFICATE-----"
        ).encode()

    @staticmethod
    def _get_root_cert(root_cert_path):
        fn = os.environ.get("APPLE_ROOT_CA")
        if fn is None:
            fn = root_cert_path or "AppleRootCA-G3.cer"

        fn = os.path.expanduser(fn)
        with open(fn, "rb") as f:
            data = f.read()
            root_cert = load_certificate(FILETYPE_ASN1, data)

        return root_cert

    @staticmethod
    def _decode_jws(token, root_cert_path, algorithms):
        try:
            return jwt.decode(
                token, algorithms=["RS256"], options={"verify_signature": False}
            )
        except (
            ValueError,
            KeyError,
            jwt.exceptions.PyJWTError,
            X509StoreContextError,
        ) as err:
            raise InvalidTokenError(err.resp.reason, vars(err))

    @staticmethod
    def parse(
        req_body, apple_root_cert_path=None, algorithms=["ES256"]
    ) -> StoreNotificationVerificationResult:
        token = req_body["signedPayload"]

        # decode main token
        payload = AppStoreNotificationVerifier._decode_jws(
            token, root_cert_path=apple_root_cert_path, algorithms=algorithms
        )

        if payload["notificationType"] == "TEST":
            return payload

        # decode signedTransactionInfo & substitute decoded into payload
        signedTransactionInfo = AppStoreNotificationVerifier._decode_jws(
            payload["data"]["signedTransactionInfo"],
            root_cert_path=apple_root_cert_path,
            algorithms=algorithms,
        )
        payload["data"]["signedTransactionInfo"] = signedTransactionInfo

        # decode signedRenewalInfo & substitute decoded into payload
        if "signedRenewalInfo" in payload["data"]:
            signedRenewalInfo = AppStoreNotificationVerifier._decode_jws(
                payload["data"]["signedRenewalInfo"],
                root_cert_path=apple_root_cert_path,
                algorithms=algorithms,
            )
            payload["data"]["signedRenewalInfo"] = signedRenewalInfo

        verification_result = {
            "notification_type": AppStoreNotificationType(
                payload.get("notificationType", None)
            ),
            "subtype": AppStoreNotificationSubtype(payload.get("subtype", None)),
            "notification_id": payload["notificationUUID"],
            "data": payload["data"],
            "notification_publish_time": datetime.datetime.utcnow(),
        }
        return StoreNotificationVerificationResult.from_verification_result(
            **verification_result
        )
