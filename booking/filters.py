from django_filters.rest_framework import FilterSet
from booking.models import BookingDose

class BookingDoseFilter(FilterSet):
    class Meta:
        model = BookingDose
        fields = {
            'status' : ['exact']
        }
