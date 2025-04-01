from rest_framework import permissions

class IsOwnerOrStaff(permissions.BasePermission):
    """
    Custom permission to allow access only to the owner of the object or staff members.
    """

    def has_object_permission(self, request, view, obj):
        # Allow safe methods for any user
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check for ownership or staff permission
        user = request.user
        if hasattr(obj, 'created_by'):
            return obj.created_by == user or user.is_staff
        elif hasattr(obj, 'user'):
            return obj.user == user or user.is_staff

        # Deny permission if no ownership attribute is found
        return False
