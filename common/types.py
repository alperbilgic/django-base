from enum import auto

from django.db import models


class FileType(models.TextChoices):
    IMAGE = auto()
    AUDIO = auto()
    VIDEO = auto()
