from rest_framework import permissions

class IsOrganizer(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):

        # Write permissions are only allowed to the owner of the object (organizer).
        return obj.organizer == request.user

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow users to edit or delete their own profiles and events.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request, so we allow GET, HEAD, or OPTIONS.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the object.
        return obj == request.user