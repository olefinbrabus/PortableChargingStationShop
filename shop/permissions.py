from rest_framework import permissions


class IsAdminAllOrIsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            and request.user
            and request.user.is_authenticated
        ) or bool(request.user.is_staff)


def permissions_read_if_anonymous(self):
    permission_classes = self.permission_classes

    if self.action in ("list", "retrieve"):
        permission_classes = {}

    return permission_classes
