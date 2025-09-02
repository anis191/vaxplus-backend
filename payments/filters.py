from django_filters.rest_framework import FilterSet
from payments.models import Payment

class PaymentsFilter(FilterSet):
    class Meta:
        model = Payment
        fields = {
            'transaction_id' : ['exact'],
            'status' : ['exact']
        }
