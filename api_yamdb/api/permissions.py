from rest_framework import permissions

from users.models import UserRoles


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return request.user.role == UserRoles.ADMIN

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == UserRoles.ADMIN


class IsAuthorOrStaffOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if (
                request.method in permissions.SAFE_METHODS
                or request.user.role == UserRoles.ADMIN
                or request.user.role == UserRoles.MODERATOR
        ):
            return True
        return obj.author == request.user
