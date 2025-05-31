from django.shortcuts import render
from campaigns.models import *
from campaigns.serializers import *
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from campaigns.filters import VaccineCampaignFilter

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(campaign_count=Count('vaccine_campaigns')).all()
    serializer_class = CategorySerializer

class VaccineViewSet(ModelViewSet):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name','description']

class VaccineCampaignViewSet(ModelViewSet):
    queryset = VaccineCampaign.objects.all()
    serializer_class = VaccineCampaignSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = VaccineCampaignFilter
    search_fields = ['title','description']
    ordering_fields = ['start_date']

class CampaignReviewViewSet(ModelViewSet):
    queryset = CampaignReview.objects.all()
    serializer_class = CampaignReviewSerializers