from enum import Enum, auto
from types import DynamicClassAttribute


class MessageCode(Enum):
    GENERAL_SUCCESS = auto()
    BASE_LOGIN_SUCCESS = auto()
    USER_LOGIN_SUCCESS = auto()
    UPLOAD_FILE_REQUEST_SUCCESS = auto()
    LIST_CONTENT_SUCCESS = auto()
    RETRIEVE_CONTENT_SUCCESS = auto()
    CREATE_CONTENT_SUCCESS = auto()
    UPDATE_CONTENT_SUCCESS = auto()
    REMOVE_CONTENT_SUCCESS = auto()
    REGISTRATION_SUCCESS = auto()

    @DynamicClassAttribute
    def value(self) -> str:
        """The value of the Enum member."""
        return "MSG_" + str(self._name_)
