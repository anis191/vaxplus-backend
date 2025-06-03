from django.shortcuts import render
from campaigns.models import *
from campaigns.serializers import *
from booking.serializers import SimpleBookingDoseSerializers, BookingDoseSerializers
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from campaigns.filters import VaccineCampaignFilter
from campaigns.paginations import DefaultPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from campaigns.permissions import IsDoctorOrReadOnly, IsPatient, IsReviewAuthorOrReadOnly

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(campaign_count=Count('vaccine_campaigns')).all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated,IsDoctorOrReadOnly]

class VaccineViewSet(ModelViewSet):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name','description']
    permission_classes = [IsDoctorOrReadOnly]
    
class VaccineCampaignViewSet(ModelViewSet):
    queryset = VaccineCampaign.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = VaccineCampaignFilter
    search_fields = ['title','description']
    ordering_fields = ['start_date']
    pagination_class = DefaultPagination

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
            campaign_id = self.kwargs['campaign_pk']
        )

    def get_serializer_context(self):
        return{'campaign_id' : self.kwargs['campaign_pk'], 'user' : self.request.user}

