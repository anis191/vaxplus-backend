from rest_framework import serializers
from booking.models import *
from campaigns.models import *
from datetime import timedelta, date, datetime
from booking.services import get_available_dates

class CenterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = ['id','name','address','city','postcode']

class SimpleBookingDoseSerializers(serializers.ModelSerializer):
    dates = serializers.ChoiceField(choices=[])
    class Meta:
        model = BookingDose
        fields = ['patient','dose_center','dates']
    
    def create(self, validated_data):
        campaign_id = self.context.get('campaign_id')
        campaign = VaccineCampaign.objects.get(pk=campaign_id)
        first_dose_dt = validated_data.pop('dates')
        first_dose_date = datetime.strptime(first_dose_dt, '%Y-%m-%d').date()
        gap = campaign.vaccine.dose_gap
        second_dose_dt = first_dose_date + timedelta(days=gap)
        
        status = campaign.status
        if status in ['Ended','Paused','Canceled']:
            raise serializers.ValidationError("This campaign is not active.")
        elif date.today() > campaign.end_date:
            raise serializers.ValidationError("Campaign already ended.")
        
        booking = BookingDose.objects.create(
            patient = validated_data['patient'],
            campaign = campaign,
            dose_center = validated_data['dose_center'],
            first_dose_date = first_dose_date,
            second_dose_date = second_dose_dt,
            # status = status
        )
        return booking

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        campaign_id = self.context['campaign_id']
        if campaign_id:
            try:
                campaign = VaccineCampaign.objects.get(pk=campaign_id)
                self.fields['dates'].choices = get_available_dates(campaign)
            except VaccineCampaign.DoesNotExist:
                return serializers.ValidationError("Campaign is not found")

class BookingDoseSerializers(serializers.ModelSerializer):
    class Meta:
        model = BookingDose
        fields = ['id','patient','campaign','dose_center','first_dose_date','second_dose_date','status']
        read_only_fields = ['first_dose_date','second_dose_date']
    
    def create(self, validated_data):
        campaign = validated_data['campaign']

        today = date.today()
        first_dose_dt = max(today,campaign.start_date)
        gap = campaign.vaccine.dose_gap
        second_dose_dt = first_dose_dt + timedelta(days=gap)

        status = campaign.status
        if status == 'Ended':
            raise serializers.ValidationError("Campaign already ended.")
        elif status == 'Paused':
            raise serializers.ValidationError("Campaign is recently paused.")
        elif status == 'Canceled':
            raise serializers.ValidationError("Campaign is canceled.")

        if first_dose_dt > campaign.end_date:
            raise serializers.ValidationError("Campaign already ended.")
        
        # booking = BookingDose.objects.create(
            # patient = patient,
            # campaign = campaign,
            # dose_center = dose_center,
            # first_dose_date = first_dose_dt,
            # second_dose_date = second_dose_dt,
            # status = status
        # )

        validated_data['first_dose_date'] = first_dose_dt
        validated_data['second_dose_date'] = second_dose_dt

        return super().create(validated_data)



