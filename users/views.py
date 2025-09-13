from rest_framework.viewsets import ModelViewSet
from users.models import User, DoctorProfile, PatientProfile
from booking.models import BookingDose, VaccinationRecord
from payments.models import Payment
from users.serializers import *
from users.paginations import PatientsPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.permissions import IsDoctorAuthorOrReadOnly, IsPatientOrAdmin, IsNotDoctorsOrAdmin, IsNotDoctorUserOrAdmin
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from users.filters import DoctorApplicationsFilter
from campaigns.models import VaccineCampaign, Vaccine
from rest_framework import generics
from rest_framework.views import APIView
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404
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
    
    def paginate_queryset(self, queryset):
        if self.request.user.is_staff:
            self.pagination_class = PatientsPagination
        else:
            self.pagination_class = None
        return super().paginate_queryset(queryset)
    
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
        # if self.action == 'assign_to_doctor':
            # return [IsAdminUser()]
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsPatientOrAdmin()]

    '''@swagger_auto_schema(
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
    )'''
    '''
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
        '''

class DoctorApplicationViewSet(ModelViewSet):
    permission_classes = [IsNotDoctorUserOrAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['user__email']
    filterset_class = DoctorApplicationsFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view',False):
            return PatientProfile.objects.none()
        
        user = self.request.user
        base_query = DoctorApplication.objects.select_related('user')
        if user.is_staff:
            return base_query
        return base_query.filter(user = user)
    
    def get_serializer_class(self):
        if self.request.user.is_staff and self.request.method in ['PUT','PATCH']:
            return DoctorApprovalSerializer
        return DoctorApplicationSerializer
    
    @swagger_auto_schema(
        operation_summary="List Doctor Applications",
        operation_description="Admin can view all applications. Normal users can view their own application only."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Retrieve Doctor Application",
        operation_description="Retrieve a single doctor application by ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Apply as Doctor",
        operation_description="Authenticated users can submit a doctor application. Users cannot apply more than once."
    )
    def create(self, request, *args, **kwargs):
        if DoctorApplication.objects.filter(user=self.request.user).exists():
            return Response({"message": "You already applyed!"},)
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Approve or Reject Doctor Application",
        operation_description="Admin users can update application status. Approving automatically updates user role and creates DoctorProfile."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update of Doctor Application",
        operation_description="Admin users can partially update application status. Approving automatically updates user role and creates DoctorProfile."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Delete Doctor Application",
        operation_description="Delete a doctor application. Only allowed for admins."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class DoctorProfileViewSet(ModelViewSet):
    queryset = DoctorProfile.objects.select_related('user').all()
    # pagination_class = DoctorsPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['user__first_name', 'user__last_name','specialization']

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

class DoctorParticipatingCampaignsListView(generics.ListAPIView):
    serializer_class = DoctorParticipatingCampaignsSerializer

    def get_queryset(self):
        doctor_pk = self.kwargs['doctor_pk']

        return VaccineCampaign.objects.filter(doctor__doctor_profile__id = doctor_pk).only('id', 'title', 'start_date', 'end_date', 'status')

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {}

        if user.is_staff:
            total_payment = Payment.objects.filter(status=Payment.SUCCESS).aggregate(total=Sum("amount"))
            data = {
                "total_users": User.objects.count(),
                "total_doctors": User.objects.filter(role=User.DOCTOR).count(),
                "total_campaigns": VaccineCampaign.objects.count(),
                "total_vaccines": Vaccine.objects.count(),
                "total_booking": BookingDose.objects.count(),
                "total_payment": total_payment["total"] or 0,
            }

        elif user.role == User.PATIENT:
            data["total_campaigns"] = VaccineCampaign.objects.count()
            data["total_booked"] = BookingDose.objects.filter(patient=user).count()
            data["total_vaccine_dose"] = VaccinationRecord.objects.filter(patient=user).count()
            total_amount = Payment.objects.filter(patient=user, status=Payment.SUCCESS).aggregate(
            total_payment=Sum("amount"))
            data["total_payment"] = total_amount["total_payment"] or 0

        elif user.role == User.DOCTOR:
            campaign_ids = list(user.involve_campaigns.values_list("id", flat=True))
            total_bookings = BookingDose.objects.filter(campaign_id__in=campaign_ids).count()
            total_payment =(
                Payment.objects.filter(campaign_id__in=campaign_ids, status=Payment.SUCCESS)
                .aggregate(total=Sum("amount"))["total"] or 0
            )
            data = {
                "involved_campaigns": len(campaign_ids),
                "all_booking": total_bookings,
                "total_payment": total_payment,
            }
        return Response(data)
