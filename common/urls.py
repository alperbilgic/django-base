from django.urls import path

from common.views import (
    TranslationViewSet,
    TranslatedFileViewSet,
)

translation_viewset = TranslationViewSet.as_view({"get": "list", "post": "create"})

translation_detail_viewset = TranslationViewSet.as_view(
    {"put": "update", "patch": "partial_update", "get": "retrieve", "delete": "destroy"}
)

translation_bulk_create_view = TranslationViewSet.as_view({"post": "bulk_create"})

translated_file_viewset = TranslatedFileViewSet.as_view(
    {"get": "list", "post": "create"}
)

translated_file_detail_viewset = TranslatedFileViewSet.as_view(
    {"put": "update", "patch": "partial_update", "get": "retrieve", "delete": "destroy"}
)

translated_file_bulk_create_view = TranslatedFileViewSet.as_view(
    {"post": "bulk_create"}
)

urlpatterns = [
    path("translation/", translation_viewset, name="translation-viewset"),
    path(
        "translation/<int:id>/",
        translation_detail_viewset,
        name="translation-detail-viewset",
    ),
    path(
        "translation/bulk_create/",
        translation_bulk_create_view,
        name="translation-bulk-create-view",
    ),
    path("translated_file/", translated_file_viewset, name="translated-file-viewset"),
    path(
        "translated_file/<int:id>/",
        translated_file_detail_viewset,
        name="translated-file-detail-viewset",
    ),
    path(
        "translated_file/bulk_create/",
        translated_file_bulk_create_view,
        name="translated-file-bulk-create-view",
    ),
]
