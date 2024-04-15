from rest_framework import permissions

from user.types import UserRole


class UserViewSetPermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        """
        Allow operations only to users themselves or upper roles than Editor
        """

        auth = request.auth
        if auth:
            jwt_payload = auth.payload
            role = UserRole(jwt_payload.get("role", None) or UserRole.NONE.value)
            if role and (role > UserRole.EDITOR):
                return True
            elif (
                role
                and (role >= UserRole.EDITOR)
                and view.action in ["list", "retrieve", "partial_update"]
            ):
                return True

            user_id = view.kwargs["user_id"]
            if user_id and user_id == jwt_payload.get("user_id", None):
                return True

        return False
