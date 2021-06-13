from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            obj == request.user
        )


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user
