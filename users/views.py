from rest_framework.viewsets import ModelViewSet
from users.models import User, DoctorProfile, PatientProfile
from users.serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.permissions import IsDoctorAuthorOrReadOnly, IsPatientOrAdmin
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class PatientProfileViewSet(ModelViewSet):
    http_method_names = ['get','put','patch','delete']
    filter_backends = [DjangoFilterBackend, SearchFilter,]
    def filter_queryset(self, queryset):
        if self.request.user.is_staff:
            self.search_fields = ['user__email']
        else:
            self.search_fields = []
        return super().filter_queryset(queryset)

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
    def get_permissions(self):
        if self.action == 'assign_to_doctor':
            return [IsAdminUser()]
        return [IsPatientOrAdmin()]

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

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsDoctorAuthorOrReadOnly()]

    def get_serializer_class(self):
        if self.request.method in ['POST','PATCH','PUT']:
            return DoctorProfileSerializers
        return SimpleDoctorSerializers
