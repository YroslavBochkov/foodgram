from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешение для авторов объектов."""

    def has_object_permission(self, request, view, obj):
        """Проверяет доступ к объекту."""
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and (obj.author == request.user)
        )
