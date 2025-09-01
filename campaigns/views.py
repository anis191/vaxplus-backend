from django.shortcuts import render
from campaigns.models import *
from campaigns.serializers import *
from booking.serializers import SimpleBookingDoseSerializers, BookingDoseSerializers
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from campaigns.filters import VaccineCampaignFilter, VaccineFilter
from campaigns.paginations import DefaultPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from campaigns.permissions import IsDoctorOrReadOnly, IsPatient, IsReviewAuthorOrReadOnly
from django.db.models import Prefetch
from drf_yasg.utils import swagger_auto_schema
#
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(campaign_count=Count('vaccine_campaigns')).all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated,IsDoctorOrReadOnly]

    @swagger_auto_schema(
    operation_summary="Browse all vaccine categories",
    operation_description="""
    Returns a list of all vaccine categories, with each category annotated with the number of related vaccine campaigns.

    - Accessible to all authenticated users.
    
    - Each category includes a `campaign_count` field.
    """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
    operation_summary="Retrieve category details",
    operation_description="""
    Returns details of a specific vaccine category, including the number of related campaigns.

    - Accessible to all authenticated users.
    """
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
    operation_summary="Create a new vaccine category",
    operation_description="""
    Allows a doctor or admin to create a new vaccine category.

    - Requires authentication.
    
    - Only doctors and admins can perform this action.
    """
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
    operation_summary="Update a vaccine category",
    operation_description="""
    Allows a doctor or admin to fully update a vaccine category.

    - Requires authentication.
    
    - Only doctors and admins can perform this action.
    """
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
    operation_summary="Partially update a vaccine category",
    operation_description="""
    Allows a doctor or admin to partially update a vaccine category.

    - Requires authentication.
    
    - Only doctors and admins can perform this action.
    """
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
    operation_summary="Partially update a vaccine category",
    operation_description="""
    Allows a doctor or admin to partially update a vaccine category.

    - Requires authentication.
    
    - Only doctors and admins can perform this action.
    """
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
    operation_summary="Delete a vaccine category",
    operation_description="""
    Deletes a vaccine category by its ID.

    - Only doctors or admins can delete a category.
    """
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class VaccineViewSet(ModelViewSet):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name','description']
    filterset_class = VaccineFilter
    permission_classes = [IsDoctorOrReadOnly]

    @swagger_auto_schema(
        operation_summary="List all vaccines",
        operation_description="""
        - Returns a list of all available vaccines.
        
        - Searchable by `name` and `description` (query param: `?search=`).
        
        - Publicly readable.
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new vaccine",
        operation_description="""
        - **Only Doctors** are allowed to create new vaccines.
        
        - Provide all required fields as defined in the serializer.
        """
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a specific vaccine",
        operation_description="""
        - View details of a specific vaccine by ID.
        
        - Readable by all users.
        """
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a vaccine",
        operation_description="""
        - Only **doctors** or **admins** can update vaccine details.
        """
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a vaccine",
        operation_description="""
        - Only **Doctors** and **admin** can partially update a vaccine record.
        """
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a vaccine",
        operation_description="""
        - Only **Doctors** and **admin** can delete a vaccine.
        """
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
class VaccineCampaignViewSet(ModelViewSet):
    # queryset = VaccineCampaign.objects.select_related('category').prefetch_related('vaccine').all()
    queryset = VaccineCampaign.objects.select_related('category').prefetch_related(Prefetch(
            'vaccine',
            queryset=Vaccine.objects.only('id', 'name', 'total_doses', 'is_booster')
        )).all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = VaccineCampaignFilter
    search_fields = ['title','description']
    ordering_fields = ['start_date']
    pagination_class = DefaultPagination

    @swagger_auto_schema(
        operation_summary="List vaccine campaigns",
        operation_description="""
        Returns a paginated list of vaccine campaigns.

        - Supports filtering by `category`,`start_date` and `status`.

        - Supports full-text search on `title` and `description`.
        
        - Supports ordering by `start_date`.
        
        - Accessible to all users.
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
    operation_summary="Create a new vaccine campaign",
    operation_description="""
    Creates a new vaccine campaign.
    - Permission: Only authenticated **doctors** and **admins** can create campaigns.
    
    - Requires all required fields.
    """
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve vaccine campaign details",
        operation_description="Returns detailed information about a specific vaccine campaign by ID."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
    operation_summary="Update a vaccine campaign",
    operation_description="""
    Fully updates a vaccine campaign.

    - Permission: Only **doctor** or **admin** can update.

    - Replaces all fields with new data.
    """
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
    operation_summary="Partially update a vaccine campaign",
    operation_description="""
    Updates one or more fields of a vaccine campaign.

    - **Permission:** Only doctor (or admin) can update.

    - Only the provided fields will be updated(Not read only fields).
    """
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
    operation_summary="Delete a vaccine campaign",
    operation_description="""
    Deletes a vaccine campaign by its ID.

    - Permission: Only **doctor** (or **admin**) can delete.

    - This action is irreversible.
    """
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Booked a dose in a vaccine campaign",
        operation_description="""
        Book a vaccination dose for the logged-in user under a specific campaign.

        - **Permissions:** Only authenticated users can book a dose.
        
        - **Request Validation:** Requires POST data validated by `SimpleBookingDoseSerializers`.
        
        - **Detail:** The user must select a valid `dose_center` and choose a `date` for the **first dose** from the available dates of the campaign.The **second dose date** is automatically assigned based on the vaccine's dose gap.
        """,
        request_body=SimpleBookingDoseSerializers
    )
    @action(detail=True, methods=['post'])
    def booked(self, request, pk=None):
        campaign = self.get_object()
        serializer = SimpleBookingDoseSerializers(
            data=request.data,
            context = self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status' : 'Booked the campaign'})
    
    def get_permissions(self):
        if self.action == 'booked':
            return [IsAuthenticated()]
        return [IsDoctorOrReadOnly()]

    def get_serializer_class(self):
        if self.action == 'booked':
            return SimpleBookingDoseSerializers
        return VaccineCampaignSerializers
    
    def get_serializer_context(self):
        return {'campaign_id' : self.kwargs.get('pk'), 'user' : self.request.user}

class CampaignReviewViewSet(ModelViewSet):
    serializer_class = CampaignReviewSerializers
    permission_classes = [IsReviewAuthorOrReadOnly]

    def get_queryset(self):
        return CampaignReview.objects.filter(
            campaign_id = self.kwargs.get('campaign_pk')
        ).select_related('patient')

    def get_serializer_context(self):
        return{'campaign_id' : self.kwargs.get('campaign_pk'), 'user' : self.request.user}
    
    @swagger_auto_schema(
        operation_summary="List all reviews of a campaign",
        operation_description="""
        Returns a list of all reviews submitted for the specified vaccine campaign.
        
        - Accessible to all users.

        - Returns review author, comment, and rating.
        """
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Create a new review",
        operation_description="""
        Creates a new review for the given vaccine campaign.
        - Permissions:
            - Only authenticated users can create reviews.
            
            - Users can only review those campaigns which they have already **booked** or **completed**.

        - Required fields:
          - `rating` (integer, 1–5)
          
          - `comment` (string)
        """,
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Retrieve a specific review",
        operation_description="""
        Retrieves details of a specific review by its ID.
        - Accessible to all users.
        """
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update a review",
        operation_description="""
        Fully updates a review. Replaces all fields.

        - Only the author of the review can perform this action.
        
        - Requires authentication.
        """
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Partially update a review",
        operation_description="""
        Updates one or more fields of a review.

        - Only the author of the review can perform this action.
        
        - Requires authentication.
        """
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Delete a review",
        operation_description="""
        Deletes a review from the specified campaign.

        - Only the author of the review can delete it.
        
        - This action is irreversible.
        """
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
class CampaignDoctorsListView(generics.ListAPIView):
    serializer_class = CampaignDoctorsSerializers
    def get_queryset(self):
        campaign_id = self.kwargs.get('pk')
        return User.objects.filter(
            role = User.DOCTOR,
            involve_campaigns__id = campaign_id
        ).select_related('doctor_profile')