from django.shortcuts import render
from campaigns.models import *
from campaigns.serializers import *
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from campaigns.filters import VaccineCampaignFilter
from campaigns.paginations import DefaultPagination

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(campaign_count=Count('vaccine_campaigns')).all()
    serializer_class = CategorySerializer

class VaccineViewSet(ModelViewSet):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name','description']

    # def get_queryset(self):
        # return Vaccine.objects.filter(campaigns=self.kwargs['campaign_pk']).all()
    

class VaccineCampaignViewSet(ModelViewSet):
    queryset = VaccineCampaign.objects.all()
    serializer_class = VaccineCampaignSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = VaccineCampaignFilter
    search_fields = ['title','description']
    ordering_fields = ['start_date']
    pagination_class = DefaultPagination


class CampaignReviewViewSet(ModelViewSet):
    # queryset = CampaignReview.objects.all()
    serializer_class = CampaignReviewSerializers

    def get_queryset(self):
        return CampaignReview.objects.filter(
            campaign_id = self.kwargs['campaign_pk']
        )

    def get_serializer_context(self):
        return{'campaign_id' : self.kwargs['campaign_pk']}