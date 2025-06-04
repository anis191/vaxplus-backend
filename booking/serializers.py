from rest_framework import serializers
from booking.models import *
from campaigns.models import *
from booking.services import BookingServices

class CenterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = ['id','name','address','city','postcode']

class SimpleBookingDoseSerializers(serializers.ModelSerializer):
    dates = serializers.ChoiceField(choices=[])
    dose_center = serializers.PrimaryKeyRelatedField(
        queryset=Center.objects.all()
    )
    class Meta:
        model = BookingDose
        fields = ['dose_center','dates']
    
    def create(self, validated_data):
        campaign_id = self.context.get('campaign_id')
        user = self.context.get('user')
        return BookingServices.create_booking_dose(validated_data=validated_data,campaign_id=campaign_id, user=user)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        campaign_id = self.context.get('campaign_id')
        if campaign_id:
            try:
                campaign = VaccineCampaign.objects.get(pk=campaign_id)
                self.fields['dates'].choices = BookingServices.get_available_dates(campaign)
            except VaccineCampaign.DoesNotExist:
                return serializers.ValidationError("Campaign is not found")

class BookingDoseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingDose
        fields = ['id','patient','campaign','dose_center','first_dose_date','second_dose_date','status']
        read_only_fields = fields

class BookingDoseSerializers(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='patient.email')
    title = serializers.ReadOnlyField(source='campaign.title')
    class Meta:
        model = BookingDose
        fields = ['id','patient','email','campaign','title','dose_center','first_dose_date','second_dose_date','status']
        read_only_fields = ['patient','campaign','dose_center','first_dose_date','second_dose_date']
    
    def validate_status(self, value):
        user = self.context.get('user')
        current_instance = getattr(self, 'instance', None)
        return BookingServices.validate_booking_status(user, current_instance, value)

class VaccinationRecordSerializers(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='patient.email')
    vaccine = serializers.ReadOnlyField(source='campaign.vaccine.name')
    class Meta:
        model = VaccinationRecord
        fields = ['id','patient','email','campaign','vaccine','dose_number','given_date']