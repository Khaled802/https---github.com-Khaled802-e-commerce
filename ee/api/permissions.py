from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_object_permission(self, request, view, obj):
        object_owner = obj.user
        currnet_user = request.user
        
        if object_owner == currnet_user:
            return True
        return bool(
            request.method in permissions.SAFE_METHODS and
            request.user and
            request.user.is_authenticated
        )