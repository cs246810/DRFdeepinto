from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

class IsUserSelfOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and obj == request.user or
            request.method in SAFE_METHODS
        )

class IsAdminOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_staff or
            request.method in SAFE_METHODS
        )