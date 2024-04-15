from django.urls import path

from .views import (
    AvatarViewSet,
    UserViewSet,
    SchoolViewSet,
    ClassViewSet,
)

user_detail = UserViewSet.as_view(
    {"patch": "partial_update", "delete": "destroy", "get": "retrieve"}
)
user_list = UserViewSet.as_view({"get": "list"})

avatar_list = AvatarViewSet.as_view({"get": "list", "post": "create"})

school_list_view = SchoolViewSet.as_view({"get": "list", "post": "create"})
school_details_view = SchoolViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

class_list_view = ClassViewSet.as_view({"get": "list", "post": "create"})
class_details_view = ClassViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    path("avatar/", avatar_list, name="avatar-viewset"),
    path("school/", school_list_view, name="school-viewset"),
    path("school/<str:id>/", school_details_view, name="school-detail-viewset"),
    path("class/", class_list_view, name="class-viewset"),
    path("class/<str:id>/", class_details_view, name="class-detail-viewset"),
    path("", user_list, name="user-viewset"),
    path("<str:user_id>/", user_detail, name="user-detail-viewset"),
]
