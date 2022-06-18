from rest_framework import permissions


class SafeOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return


class UserIsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id


class RoleIsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'Admin'


class RoleIsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'Moderator'


class RoleIsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'User'
