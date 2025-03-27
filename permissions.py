from rest_framework import permissions

class IsOwnerOrStaff(permissions.BasePermission):
    """
    Custom permission to allow access only to the owner of the object or staff members.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS (e.g., GET, HEAD, OPTIONS) are allowed for any user
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permissions are only allowed to the owner or staff
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user or request.user.is_staff
        elif hasattr(obj, 'user'):
            return obj.user == request.user or request.user.is_staff

        # Default to denying permission if no ownership attribute is found
        return False