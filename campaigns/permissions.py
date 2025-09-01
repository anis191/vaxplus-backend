from rest_framework import permissions

class IsDoctorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            request.user.is_authenticated and (
                request.user.role == 'Doctor' or request.user.is_staff
            )
        )
    
    # Resone: Only those doctors can edit a campaign, who involved on this vaccine campaign
    # def has_object_permission(self, request, view, obj):
        # if request.method in permissions.SAFE_METHODS:
            # return True
        # if request.user.is_staff:
            # return True
        # return obj.doctor.filter(id=request.user.id).exists()

class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == 'Patient')

class IsReviewAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.is_staff:
            return True
        return obj.patient == request.user
