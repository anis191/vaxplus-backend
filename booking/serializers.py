from rest_framework import serializers
from booking.models import *
from campaigns.models import *
from datetime import timedelta, date, datetime
from booking.services import BookingServices

class CenterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = ['id','name','address','city','postcode']

class SimpleBookingDoseSerializers(serializers.ModelSerializer):
    dates = serializers.ChoiceField(choices=[])
    class Meta:
        model = BookingDose
        fields = ['dose_center','dates']
    
    def create(self, validated_data):
        campaign_id = self.context.get('campaign_id')
        user = self.context.get('user')
        return BookingServices.create_booking_dose(validated_data=validated_data,campaign_id=campaign_id, user=user)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        campaign_id = self.context['campaign_id']
        if campaign_id:
            try:
                campaign = VaccineCampaign.objects.get(pk=campaign_id)
                self.fields['dates'].choices = BookingServices.get_available_dates(campaign)
            except VaccineCampaign.DoesNotExist:
                return serializers.ValidationError("Campaign is not found")

class BookingDoseSerializers(serializers.ModelSerializer):
    class Meta:
        model = BookingDose
        fields = ['id','patient','campaign','dose_center','first_dose_date','second_dose_date','status']
        read_only_fields = ['first_dose_date','second_dose_date']

class VaccinationRecordSerializers(serializers.ModelSerializer):
    class Meta:
        model = VaccinationRecord
        fields = ['id','patient','campaign','dose_number','given_date']