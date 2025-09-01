from django_filters.rest_framework import FilterSet, DateFromToRangeFilter, NumberFilter
from campaigns.models import VaccineCampaign, Vaccine
from users.models import PatientProfile

class VaccineFilter(FilterSet):
    user_age = NumberFilter(method='filter_by_age')
    class Meta:
        model = Vaccine
        fields = {}
    
    def filter_by_age(self, queryset, name, value):
        return queryset.filter(
            min_age__lte=value,
            max_age__gte=value
        )

class VaccineCampaignFilter(FilterSet):
    class Meta:
        model = VaccineCampaign
        fields = {
            'category_id' : ['exact'],
            'start_date' : ['gt','lt'],
            'status' : ['exact'],
        }
