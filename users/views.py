from rest_framework.viewsets import ModelViewSet
from users.models import User, DoctorProfile, PatientProfile
from users.serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.permissions import IsDoctorAuthorOrReadOnly, IsPatientOrAdmin
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(detail=True, methods=['post'])
    def assign_to_doctor(self, request, pk=None):
        patient = self.get_object()
        user = patient.user
        if user.role == 'Doctor':
            return Response({"message" : "This user is not a patient."})
        user.role = 'Doctor'
        user.save()
        DoctorProfile.objects.get_or_create(user = user)
        patient.delete()

        return Response({"message": "User has been assign to doctor."})

class DoctorProfileViewSet(ModelViewSet):
    queryset = DoctorProfile.objects.all()
    # serializer_class = DoctorProfileSerializers
    # permission_classes = [IsDoctorAuthorOrReadOnly]
    '''def get_queryset(self):
        user = self.request.user

        if user.role == User.DOCTOR:
            return DoctorProfile.objects.filter(user=user)
        
        return DoctorProfile.objects.all()'''

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsDoctorAuthorOrReadOnly()]

    def get_serializer_class(self):
        if self.request.method in ['POST','PATCH','PUT']:
            return DoctorProfileSerializers
        return SimpleDoctorSerializers
