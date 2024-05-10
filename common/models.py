from typing import Dict, List

from django.conf import settings
from django.db import models, transaction
from django.db.models import Q, Subquery, F, Prefetch
from django_softdelete.models import SoftDeleteModel

from cloud_storage.constants.file_upload_constants import (
    get_storage_bucket,
    get_content_type_from_extension,
)
from cloud_storage.get_cloud_storage_client import (
    get_cloud_storage_client,
    get_cloud_storage_vendor,
)
from cloud_storage.idrive_client import CloudRequest
from common.types import FileType, LocaleCode
from utils.converters import ModelConverter
from utils.fields import DateTimeWithoutTZField


class Locale(models.Model):
    name = models.CharField(max_length=150, blank=False, null=False, unique=True)
    code = models.CharField(
        max_length=16,
        choices=LocaleCode.choices,
        blank=False,
        null=False,
        unique=True,
        default=LocaleCode.EN.value,
    )
    created = DateTimeWithoutTZField(auto_now_add=True, editable=False, null=True)
    updated = DateTimeWithoutTZField(auto_now=True, editable=False, null=True)

    class Meta:
        db_table = "locale"

    @classmethod
    def get_default(cls) -> "Locale":
        locale, created = cls.objects.get_or_create(
            name="Turkey",
            code="tr",
        )
        return locale

    @classmethod
    def get_default_id(cls) -> "Locale":
        locale, created = cls.objects.get_or_create(
            name="Turkey",
            code="tr",
        )
        return locale.id

    @classmethod
    def get_default_english(cls) -> "Locale":
        locale, created = cls.objects.get_or_create(
            name="England",
            code="en",
        )
        return locale


class TranslationManager(models.Manager):
    def get_queryset(self):
        return super(TranslationManager, self).get_queryset().select_related("root")


class Translation(SoftDeleteModel):
    text = models.CharField(max_length=512, null=False, blank=False)
    root = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="translations",
        null=True,
        blank=True,
    )
    locale = models.ForeignKey(
        Locale,
        on_delete=models.CASCADE,
        related_name="translations",
        default=Locale.get_default_id,
    )
    created = DateTimeWithoutTZField(auto_now_add=True, editable=False)
    updated = DateTimeWithoutTZField(auto_now=True, editable=False)
    deleted_at = DateTimeWithoutTZField(blank=True, null=True)

    class Meta:
        db_table = "translation"
        constraints = [
            models.UniqueConstraint(
                fields=["root", "locale"],
                condition=Q(deleted_at__isnull=True),
                name="unique_root_id_locale_id_if_not_deleted",
            ),
            models.UniqueConstraint(
                fields=["locale", "text"],
                condition=Q(deleted_at__isnull=True),
                name="unique_locale_id_text_if_not_deleted",
            ),
        ]

    @transaction.atomic
    def delete(self, using=None, keep_parents=False):
        if self.root_id is None or self.root_id == self.id:
            # Delete all translations that have the current instance as root
            # except the current instance itself to avoid recursion
            self.translations.exclude(id=self.id).delete()

        super(Translation, self).delete(using=using, keep_parents=keep_parents)

    @transaction.atomic
    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        is_create = not bool(self.id)
        super().save(force_insert, force_update, using, update_fields)
        if is_create and self.root_id is None:
            self.root_id = self.id
            self.save()

    def get_text_by_locale_code_or_default(self, locale_code: str) -> str:
        original_translation = self.root
        translation = (
                original_translation.translations.filter(locale__code=locale_code).first()
                or original_translation.translations.filter(locale__code="en").first()
                or original_translation.translations.first()
        )
        return translation.text if translation else ""

    @staticmethod
    def get_list_of_texts_from_id_list(
            translation_ids: List, locale_code: str
    ) -> Dict[int, str]:
        """
        Returns translated texts of given inputs
        """
        translation_text_match = {}

        def update_translation_match(root_id: int, id: int, text: str):
            translation_text_match.update({root_id: text, id: text})

        root_ids = (
            Translation.objects.filter(id__in=translation_ids)
            .values_list("root_id", flat=True)
            .all()
        )
        translations = Translation.objects.filter(
            root_id__in=Subquery(root_ids), locale__code=locale_code
        )
        for translation in translations:
            update_translation_match(
                translation.root_id, translation.id, translation.text
            )
        missing_translation_ids = [
            translation_id
            for translation_id in translation_ids
            if translation_text_match.get(translation_id, None) is None
        ]
        missing_translations = Translation.objects.filter(
            id__in=missing_translation_ids
        ).select_related("root")
        for missing_translation in missing_translations:
            translation_text_match.update(
                {missing_translation.id: missing_translation.root.text}
            )
        return translation_text_match

    @staticmethod
    def create_prefetch_for_language(language_code, field_route, **kwargs) -> Prefetch:
        translations = Translation.objects.filter(locale__code=language_code)
        return Prefetch(field_route, queryset=translations)


class TranslatedFile(SoftDeleteModel):
    name = models.CharField(max_length=255, blank=False, null=True)
    extension = models.CharField(max_length=64, null=False, blank=False)
    vendor_url = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        default=get_cloud_storage_client().endpoint,
    )
    bucket_name = models.CharField(
        max_length=255, null=False, blank=False, default=get_storage_bucket
    )
    directory = models.CharField(
        max_length=2048,
        null=False,
        blank=False,
        default=settings.TRANSLATED_FILE_DIRECTORY,
    )
    type = models.CharField(
        max_length=64, choices=FileType.choices, null=False, blank=False
    )
    vendor = models.CharField(
        max_length=64, null=False, blank=False, default=get_cloud_storage_vendor
    )
    public = models.BooleanField(
        null=False,
        blank=False,
        default=True,
    )
    root = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="translations",
        null=True,
        blank=True,
    )
    locale = models.ForeignKey(
        Locale,
        on_delete=models.CASCADE,
        related_name="translated_files",
        default=Locale.get_default_id,
    )
    created = DateTimeWithoutTZField(auto_now_add=True, editable=False)
    updated = DateTimeWithoutTZField(auto_now=True, editable=False)
    deleted_at = DateTimeWithoutTZField(blank=True, null=True)

    class Meta:
        db_table = "translated_file"
        constraints = [
            models.UniqueConstraint(
                fields=["root", "locale"],
                condition=Q(deleted_at__isnull=True),
                name="unique_translated_file_root_id_locale_id_if_not_deleted",
            ),
            models.CheckConstraint(
                check=Q(name__isnull=True) & ~Q(root_id=F("id"))
                      | (Q(name__isnull=False) & Q(root_id=F("id"))),
                name="translated_file_not_null_name_if_root",
            ),
        ]

    @transaction.atomic
    def delete(self, using=None, keep_parents=False):
        if self.root_id is None or self.root_id == self.id:
            # Delete all translations that have the current instance as root
            # except the current instance itself to avoid recursion
            self.translations.exclude(id=self.id).delete()

        super(TranslatedFile, self).delete(using=using, keep_parents=keep_parents)

    @transaction.atomic
    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        is_create = not bool(self.id)
        super().save(force_insert, force_update, using, update_fields)
        if is_create and self.root_id is None:
            self.root_id = self.id
            self.save()

    @property
    def url(self):
        if self.public:
            return f"{self.vendor_url}/{self.bucket_name}/{self.file_path}"
        client = get_cloud_storage_client(self.vendor, self.vendor_url)
        return client.create_presigned_url(str(self.bucket_name), str(self.file_path))

    @property
    def file_path(self):
        return f"{self.directory}{self.id}.{self.extension}"

    def get_upload_url(self, expiration: int = None):
        client = get_cloud_storage_client(self.vendor, self.vendor_url)
        if not self.public:
            return client.create_presigned_url(
                str(self.bucket_name),
                str(self.file_path),
                expiration,
                CloudRequest.Upload,
                content_type=get_content_type_from_extension(self.extension),
            )
        else:
            return client.create_presigned_url(
                str(self.bucket_name),
                str(self.file_path),
                None,
                CloudRequest.Upload,
                content_type=get_content_type_from_extension(self.extension),
            )

    def to_dict(self):
        page_file_dict = ModelConverter.model_to_dict(self)
        page_file_dict["url"] = self.url
        return page_file_dict

    @staticmethod
    def get_list_of_urls_from_id_list(
            translation_ids: List, locale_code: str
    ) -> Dict[int, str]:
        """
        Returns translated texts of given inputs
        """
        translation_url_match = {}

        def update_translation_match(root_id: int, id: int, url: str):
            translation_url_match.update({root_id: url, id: url})

        root_ids = (
            TranslatedFile.objects.filter(id__in=translation_ids)
            .values_list("root_id", flat=True)
            .all()
        )
        translations = TranslatedFile.objects.filter(
            root_id__in=Subquery(root_ids), locale__code=locale_code
        )
        for translation in translations:
            update_translation_match(
                translation.root_id, translation.id, translation.url
            )
        missing_translation_ids = [
            translation_id
            for translation_id in translation_ids
            if translation_url_match.get(translation_id, None) is None
        ]
        missing_translations = TranslatedFile.objects.filter(
            id__in=missing_translation_ids
        ).select_related("root")
        for missing_translation in missing_translations:
            translation_url_match.update(
                {missing_translation.id: missing_translation.root.url}
            )
        return translation_url_match
