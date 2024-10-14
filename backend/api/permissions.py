from rest_framework import permissions

from users.models import ADMIN, MODERATOR


class IsAdminPermission(permissions.BasePermission):
    """Разрешает действия только админу или суперпользователю."""
    def has_permission(self, request, view):
        request.user.has_access = ADMIN
        return request.user.is_authenticated and request.user.has_access