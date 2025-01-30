from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user or request.user.is_superuser
    
    #Adds view level permissions to owners and superusers
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class IsSuperUser(permissions.BasePermission):
    #Custom permissions to ensure SuperUsers can view all content
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser
    
class IsAuthenticatedReadOnly(permissions.BasePermission):
    #Custom permissions to ensure all authenticated users can view content on the Board
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool and request.user.is_authenticated
        # Require Superuser for all other actions other than viewing
        return bool(request.user and request.user.is_superuser)