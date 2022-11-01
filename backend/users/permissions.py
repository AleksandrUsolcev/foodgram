from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        elif request.method not in permissions.SAFE_METHODS:
            return request.user.is_staff
        return False


class OwnerOrAdminDestroyPatch(permissions.BasePermission):

    def has_permission(self, request, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method not in permissions.SAFE_METHODS:
            return True
