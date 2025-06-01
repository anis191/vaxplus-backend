from datetime import timedelta, date, datetime
from campaigns.models import *
from booking.models import *
from rest_framework.exceptions import ValidationError

class BookingServices:

    @staticmethod
    def get_available_dates(campaign):
        start = max(date.today(), campaign.start_date)
        end = campaign.end_date
        available_dates = []
        current = start
        if (end-start).days < 10:
            date_str = end.strftime('%Y-%m-%d')
            label = end.strftime('%B %d, %Y')
            available_dates.append((date_str, label))
            return available_dates
        else:
            while current <= end:
                date_str = current.strftime('%Y-%m-%d')
                label = current.strftime('%B %d, %Y')
                available_dates.append((date_str, label))
                current += timedelta(days=10)
            return available_dates
    
    @staticmethod
    def create_booking_dose(validated_data, campaign_id):
        campaign = VaccineCampaign.objects.get(pk=campaign_id)
        first_dose_dt = validated_data.pop('dates')
        first_dose_date = datetime.strptime(first_dose_dt, '%Y-%m-%d').date()
        gap = campaign.vaccine.dose_gap
        second_dose_dt = first_dose_date + timedelta(days=gap)
        
        status = campaign.status
        if status in ['Ended','Paused','Canceled']:
            raise ValidationError("This campaign is not active.")
        elif date.today() > campaign.end_date:
            raise ValidationError("Campaign already ended.")
        
        booking = BookingDose.objects.create(
            patient = validated_data['patient'],
            campaign = campaign,
            dose_center = validated_data['dose_center'],
            first_dose_date = first_dose_date,
            second_dose_date = second_dose_dt,
            # status = status
        )
        return booking
