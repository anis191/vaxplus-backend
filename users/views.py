from rest_framework.viewsets import ModelViewSet
from users.models import User, DoctorProfile, PatientProfile
from users.serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.permissions import IsDoctorAuthorOrReadOnly, IsPatientOrAdmin
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from drf_yasg.utils import swagger_auto_schema

class PatientProfileViewSet(ModelViewSet):
    http_method_names = ['get','post','put','patch','delete']
    filter_backends = [DjangoFilterBackend, SearchFilter,]
    def filter_queryset(self, queryset):
        if self.request.user.is_staff:
            self.search_fields = ['user__email']
        else:
            self.search_fields = []
        return super().filter_queryset(queryset)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view',False):
            return PatientProfile.objects.none()
        
        user = self.request.user
        base_query = PatientProfile.objects.select_related('user')
        if user.is_staff:
            return base_query
        
        return base_query.filter(
            user = self.request.user
        )
    
    @swagger_auto_schema(
        operation_summary="List patient profiles",
        operation_description="""
        - **Patients**: View only their own profile.
        
        - **Admins**: View all patient profiles.
        
        - Admins can search by user email using `?search=email@example.com`.
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a patient profile",
        operation_description="""
        - **Patients**: Retrieve their own profile.
        
        - **Admins**: Retrieve any patient's profile.
        """
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a patient profile",
        operation_description="""
        - **This endpoint is rarely used manually.**
        
        - A `PatientProfile` is automatically created when a new user registers in the system.
        
        - This endpoint exists for add extra info about them.

        **Default Behavior on Registration:**
        
        - All newly registered users are assigned the `Patient` role.
        
        - A `PatientProfile` is created automatically right after registration.

        **Permissions:**
        
        - Any authenticated user can access this endpoint and access own profile.
        
        - However, typical usage is handled automatically via signals or registration logic.
        """
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a patient profile",
        operation_description="""
        - **Patients**: Can update their own profile.
        
        - **Admins**: Can update any patient profile.
        """
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a patient profile",
        operation_description="""
        - Allows updating selected fields.
        
        - Same permissions as full update.
        """
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a patient profile",
        operation_description="""
        - **Patients**: Can delete their own profile.
        
        - **Admins**: Can delete any patient profile.
        """
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)
    
    serializer_class = PatientProfileSerializers
    def get_permissions(self):
        if self.action == 'assign_to_doctor':
            return [IsAdminUser()]
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsPatientOrAdmin()]

    @swagger_auto_schema(
        operation_summary="Assign a patient to doctor (Admin only)",
        operation_description="""
        ### Admin-only action

        This converts a user from `Patient` to `Doctor` role.

        ### Workflow:
        1. Admin searches the patient using `/api/v1/patients/?search=email@example.com`
        
        2. Admin calls: `POST /api/v1/patients/{id}/assign_to_doctor/`
        
        3. The following happens automatically:
           
           - User role is updated to `Doctor`
           
           - A `DoctorProfile` is created and added to the `doctors` list
           
           - The existing `PatientProfile` is deleted and no longer included in the `patients` list.
           
           - The user no longer appears in the patients list, but appears in doctors
        """
    )
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
    queryset = DoctorProfile.objects.select_related('user').all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsDoctorAuthorOrReadOnly()]

    def get_serializer_class(self):
        if self.request.method in ['POST','PATCH','PUT']:
            return DoctorProfileSerializers
        return SimpleDoctorSerializers
    
    @swagger_auto_schema(
    operation_summary="List all doctor profiles",
    operation_description="""
        Returns a list of doctor profiles.

        - Anyone (including patients) can view doctor profiles.
        
        - This includes basic public information about the doctor.
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a specific doctor profile",
        operation_description="""
        Fetch a specific doctor's profile using their ID.

        - Anyone can view this.
        """
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a doctor profile",
        operation_description="""
        Create a new profile for a doctor.

        - Only admins can create a doctor profile.
        """
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a doctor profile",
        operation_description="""
        Fully update the doctor's profile.

        - Only the doctor (author) or admin can perform this.
        
        - Replaces the full profile data.
        """
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a doctor profile",
        operation_description="""
        Partially update the profile of a doctor.
        
        - Only the doctor (author) or admin can perform this.
        """
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a doctor profile",
        operation_description="""
        Deletes a doctor profile.

        - Only the doctor (author) or admin can perform this.
        """
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
