from rest_framework import permissions

class IsAdminOrReadOnlyPermission(permissions.BasePermission):
    """
    Разрешает доступ к объектам для всех пользователей,
    но изменение или удаление доступно только админу.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.role == 'ADMIN'))

class IsAdminAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешает доступ к объектам для всех пользователей,
    но изменение доступно только автору или админу.
    """
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.creator == request.user
                or request.user.role == 'ADMIN')

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'USER']
