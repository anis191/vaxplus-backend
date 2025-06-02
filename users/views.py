from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.permissions import IsDoctorAuthorOrReadOnly, IsPatientOrAdmin

# class UserViewSet(ModelViewSet):
    # queryset = User.objects.all()
    # serializer_class = UserSerializers

class PatientProfileViewSet(ModelViewSet):
    # queryset = PatientProfile.objects.all()
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return PatientProfile.objects.all()
        
        return PatientProfile.objects.filter(
            user = self.request.user
        )
    
    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)
    
    serializer_class = PatientProfileSerializers
    permission_classes = [IsPatientOrAdmin]

class DoctorProfileViewSet(ModelViewSet):
    queryset = DoctorProfile.objects.all()
    # serializer_class = DoctorProfileSerializers
    permission_classes = [IsDoctorAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['POST','PATCH']:
            return DoctorProfileSerializers
        return SimpleDoctorSerializers
