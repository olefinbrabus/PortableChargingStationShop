from rest_framework import permissions


class IsAdminAllOrIsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            and request.user
            and request.user.is_authenticated
        ) or bool(request.user.is_staff)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in permissions.SAFE_METHODS or request.user.is_staff)
