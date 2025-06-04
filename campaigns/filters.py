from django_filters.rest_framework import FilterSet, DateFromToRangeFilter
from campaigns.models import VaccineCampaign, Vaccine
from users.models import PatientProfile

class VaccineCampaignFilter(FilterSet):
    class Meta:
        model = VaccineCampaign
        fields = {
            'category_id' : ['exact'],
            'start_date' : ['gt','lt'],
            'status' : ['exact'],
        }
