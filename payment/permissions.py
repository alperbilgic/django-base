from rest_framework import permissions

from user.types import UserRole


class ReferenceCodePermission(permissions.BasePermission):
    """
    Global permission check for editor and upper roles
    """

    def has_permission(self, request, view):
        auth = request.auth
        if view.action in ["verify_reference_code"]:
            return True

        if auth:
            jwt_payload = auth.payload
            role = UserRole(jwt_payload.get("role", None) or UserRole.NONE.value)
            if role and role >= UserRole.EDITOR:
                return True
        return False
