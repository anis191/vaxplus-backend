from django_filters.rest_framework import FilterSet
from users.models import DoctorApplication

class DoctorApplicationsFilter(FilterSet):
    class Meta:
        model = DoctorApplication
        fields = {
            'status' : ['exact']
        }
