from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from booking.serializers import *
from campaigns.permissions import IsDoctorOrReadOnly
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from drf_yasg.utils import swagger_auto_schema

class CenterViewSet(ModelViewSet):
    queryset = Center.objects.all()
    serializer_class = CenterSerializers
    permission_classes = [IsDoctorOrReadOnly]

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
        base_query = BookingDose.objects.select_related('patient','campaign','dose_center')
        if user.is_staff or user.role == 'Doctor':
            return base_query
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
    operation_summary="Update the status of a booked vaccine campaign dose",
    operation_description="""
    This endpoint allows updating the status of a booked vaccine campaign dose based on the user's role.
    
    ### Use Case & Workflow
    
    - This view handles **only `Booked` campaigns**.
    
    - **Patients**:
      - Can only see **their own booked doses**.

      - Can update their booking status **from `Booked` to `Canceled` only**.
    
    - **Doctors**:
      - Can view **all patient bookings**.

      - Can **search by patient email** using the `?search=` query param.

        - Example: `/api/v1/booking_doses/?search=patient5@gmail.com`
      
      - After confirming that a patient has received all required doses, the doctor can:
        
        - Visit the booking detail endpoint by `id`(uuid):
          
          `/api/v1/booking_doses/{uuid}/`
        
        - **Change the status from `Booked` to `Completed`.**
    
    ### System Behavior
    
    - When a doctor changes the booking status to `Completed`:
      
      - A new record is automatically created in `vaccination_records`, storing the patient's completed vaccination history.
      
      - The entry is then **deleted** from the `booking_doses`.
      
      - The booking will **no longer appear** in `booking_doses`.
    
    ### Permissions:
    - **Patient** Can only update own bookings → `Canceled`
    
    - **Doctor** Can search and update bookings → `Completed`
    
    - **Admin** Can perform full updates without restriction
    """
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

class VaccinationRecordViewSet(ModelViewSet):
    http_method_names = ['get','head','options']
    serializer_class = VaccinationRecordSerializers
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view',False):
            return VaccinationRecord.objects.none()

        user = self.request.user
        base_query = VaccinationRecord.objects.select_related('patient','campaign','campaign__vaccine')
        if user.is_staff:
            return base_query
        return base_query.filter(patient=self.request.user)

