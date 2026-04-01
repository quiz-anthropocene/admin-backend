from rest_framework.permissions import BasePermission


class IsAdministrator(BasePermission):
    """
    Grants access only to authenticated users with the ADMINISTRATOR role.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.has_role_administrator)
