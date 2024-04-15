import settings
from common.custom_exceptions.custom_exception import CustomException
from common.response.response_information_codes.error_code import ErrorCode

FILE_EXTENSION_TO_CONTENT_TYPE_MAPPER = {
    "mp3": "audio/mpeg",
    "wave": "audio/wave",
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "svg+xml": "image/svg",
    "png": "image/png",
    "mp4": "video/mp4",
}


def get_content_type_from_extension(ext: str) -> str:
    try:
        ext = ext.lower()
        return FILE_EXTENSION_TO_CONTENT_TYPE_MAPPER[ext]
    except Exception as e:
        raise CustomException.from_exception(e, code=ErrorCode.INVALID_INPUT)


def get_storage_bucket(public: bool = None) -> str:
    if public is None:
        public = settings.CLOUD_STORAGE_BUCKET_IS_PUBLIC

    return (
        settings.CLOUD_STORAGE_PUBLIC_BUCKET_NAME
        if public
        else settings.CLOUD_STORAGE_BUCKET_NAME
    )
