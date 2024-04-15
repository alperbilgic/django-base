from django.conf import settings

from cloud_storage.idrive_client import IDriveClient


def get_cloud_storage_vendor():
    return settings.CLOUD_STORAGE_VENDOR


def get_cloud_storage_client(
    cloud_storage_vendor: str = None, vendor_endpoint: str = None
):
    cloud_storage_vendor = cloud_storage_vendor or settings.CLOUD_STORAGE_VENDOR

    if cloud_storage_vendor == "idrive":
        return IDriveClient(
            vendor_endpoint or settings.IDRIVE_ENDPOINT_URL,
            settings.IDRIVE_ACCESS_KEY,
            settings.IDRIVE_SECRET_ACCESS_KEY,
        )
