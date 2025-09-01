from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from booking.serializers import *
from campaigns.permissions import IsDoctorOrReadOnly
from campaigns.paginations import VaccinationRecordPagination
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from booking.filters import BookingDoseFilter
from drf_yasg.utils import swagger_auto_schema

class CenterViewSet(ModelViewSet):
    queryset = Center.objects.all()
    serializer_class = CenterSerializers
    permission_classes = [IsDoctorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name','address','city']

    @swagger_auto_schema(
        operation_summary="List all vaccination centers",
        operation_description="""
        Returns a list of all registered vaccine dose centers.

        - Accessible to all users (read-only).

        - Each center includes its name, location, and related details.
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve center details",
        operation_description="""
        Returns the details of a specific vaccine dose center by its ID.

        - Accessible to all users (read-only).
        """
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new vaccination center",
        operation_description="""
        Allows a doctor or admin to create a new vaccine dose center.

        - Requires authentication.
        
        - Only doctors or admins can perform this action.
        """
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a vaccination center",
        operation_description="""
        Allows a doctor or admin to fully update an existing center.

        - Requires authentication.
        
        - Only doctors or admins can perform this action.
        """
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a vaccination center",
        operation_description="""
        Allows a doctor or admin to partially update the information of a center.

        - Requires authentication.
        
        - Only doctors or admins can perform this action.
        """
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a vaccination center",
        operation_description="""
        Deletes a vaccine dose center by its ID.

        - Only doctors or admins can perform this action.
        """
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class BookingDoseViewSet(ModelViewSet):
    http_method_names = ['get', 'put', 'head', 'options']
    serializer_class = BookingDoseSerializers
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter,]
    filterset_class = BookingDoseFilter

    def filter_queryset(self, queryset):
        if self.request.user.is_staff or self.request.user.role == User.DOCTOR:
            self.search_fields = ['patient__email']
        else:
            self.search_fields = []
        return super().filter_queryset(queryset)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view',False):
            return BookingDose.objects.none()
        
        user = self.request.user
        base_query = BookingDose.objects.select_related('patient','campaign','dose_center','vaccine')
        if user.is_staff:
            return base_query
        if user.role == 'Doctor':
            return base_query.filter(campaign__in = user.involve_campaigns.all())
        return base_query.filter(patient=user)
    
    def get_serializer_context(self):
        return {'campaign_id' : self.kwargs.get('pk'), 'user': self.request.user}
    
    @swagger_auto_schema(
        operation_summary="List all booked doses",
        operation_description="""
        Returns a list of all booked doses.

        - Authenticated patients will only see their own bookings.
        
        - **Doctors** and **Admins** can view all bookings.

        - Supports searching by patient `email` (**for staff and doctors only**).
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Retrieve a specific booked dose",
        operation_description="""
        Returns details of a specific booked dose by its ID.

        - Authenticated patients can only access their own bookings.
        
        - Doctors and admins can retrieve any booking.
        """
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update booking dose status",
        operation_description="""
        Update the status of a booked vaccine dose based on your role and campaign involvement.

        ### Roles & Permissions

        - **Patient**:
          - Can only update **their own bookings**.
          - Allowed status change: `Booked` → `Canceled`.

        - **Doctor**:
          - Can manage bookings **only for campaigns they are involved in**.
          - Allowed status transitions:
            - `Booked` → `First Dose Completed`
            - `First Dose Completed` → `Second Dose Completed` (if booster scheduled) or `Completed`
            - `Second Dose Completed` → `Completed` (if booster scheduled)
          - Cannot view or update bookings outside their campaigns.

        - **Admin/Staff**:
          - Can perform full updates without restriction.

        ### System Behavior

        - When a booking is marked as `First Dose Completed`, `Second Dose Completed`, or `Completed`:
          - A corresponding record is automatically added to **VaccinationRecord**.

        - When a booking is marked as `Completed`:
          - The booking is automatically **deleted** from `booking_doses`.
          - The booking will no longer appear in list endpoints.

        ### Usage Example

        - Endpoint: `PUT /api/v1/booking_doses/{uuid}/`
        - Request Body Example:
        ```json
        {
            "status": "Canceled"
        }
        ```
        - Doctors can only update bookings related to their own campaigns.

        - Patients can only update their own bookings.
        """
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

class VaccinationRecordViewSet(ModelViewSet):
    http_method_names = ['get','head','options']
    serializer_class = VaccinationRecordSerializers
    permission_classes=[permissions.IsAuthenticated]
    pagination_class = VaccinationRecordPagination
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    ordering_fields = ['given_date']

    def filter_queryset(self, queryset):
        if self.request.user.is_staff:
            self.search_fields = ['patient__email']
        else:
            self.search_fields = []
        return super().filter_queryset(queryset)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view',False):
            return VaccinationRecord.objects.none()

        user = self.request.user
        base_query = VaccinationRecord.objects.select_related('patient','campaign','vaccine')
        if user.is_staff:
            return base_query
        return base_query.filter(patient=self.request.user)
    
    @swagger_auto_schema(
        operation_summary="List vaccination records",
        operation_description="""
        - **Admin** users can view **all** patients vaccination records.
        
        - **Patients** can view **only their own** vaccination history.
        
        - **These records are auto-generated when a doctor marks a booking as 'Completed'.**
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a specific vaccination record",
        operation_description="""
        - **Admin** users can view any patient’s vaccination record detail.
        
        - **Patients** can view only their own vaccination record detail.
        
        - Vaccination records are read-only and reflect completed campaigns.
        """
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

