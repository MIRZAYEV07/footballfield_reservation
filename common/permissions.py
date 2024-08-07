from rest_framework import permissions


class UpdateDeletePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # if obj.owner == request.user and request.user.is_moderator:
        if request.user.is_field_owner:
            return True
        return False


class CreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_field_owner:
           return True
        return False


class DeletePersonalObjectPermission(permissions.BasePermission):
    # pass
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class PersonalObjectPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.id == request.user.id:
            return True
        return False


class UpdatePermission(permissions.BasePermission):
    # pass
    def has_object_permission(self, request, view, obj):
        if obj.id == request.user.id:
            return True
        return False