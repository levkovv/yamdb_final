from rest_framework import permissions

from .models import UserRoles


class IsAdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return (request.user.role == UserRoles.ADMIN
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return (request.user.role == UserRoles.ADMIN
                or request.user.is_superuser)
