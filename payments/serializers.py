from rest_framework import serializers
from payments.models import Payment
#
class PaymentSerializer(serializers.ModelSerializer):
    title = serializers.ReadOnlyField(source='campaign.title')
    class Meta:
        model = Payment
        fields = ['id','patient','campaign','title','amount','transaction_id','created_at','status']
