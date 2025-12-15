from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return getattr(obj, "author_id", None) == request.user.id
    
from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Follow

class CanViewProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not obj.is_private:
            return True
        if obj.id == request.user.id:
            return True
        return Follow.objects.filter(
            follower=request.user, following=obj, status=Follow.ACCEPTED
        ).exists()
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return getattr(obj, "id", None) == request.user.id
    