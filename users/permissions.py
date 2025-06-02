from rest_framework import permissions

from rest_framework import permissions

class IsDoctorAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True
        
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True
        
        if request.user.is_staff:
            return True
        return obj.user == request.user

class IsPatientOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and (request.user.role == 'Patient' or request.user.is_staff))
