from enum import auto

from django.db import models


class LocaleCode(models.TextChoices):
    TR = "tr"
    EN = "en"


class FileType(models.TextChoices):
    IMAGE = auto()
    AUDIO = auto()
    VIDEO = auto()
