from django.shortcuts import render
from campaigns.models import *
from campaigns.serializers import *
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(campaign_count=Count('vaccine_campaigns')).all()
    serializer_class = CategorySerializer

class VaccineViewSet(ModelViewSet):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializers

class VaccineCampaignViewSet(ModelViewSet):
    queryset = VaccineCampaign.objects.all()
    serializer_class = VaccineCampaignSerializers

class CampaignReviewViewSet(ModelViewSet):
    queryset = CampaignReview.objects.all()
    serializer_class = CampaignReviewSerializers