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
    def create_booking_dose(validated_data, campaign_id, user):
        campaign = VaccineCampaign.objects.get(pk=campaign_id)

        if BookingDose.objects.filter(patient=user, campaign=campaign).exists():
            raise ValidationError("You already booked this campaign!")

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
            patient = user,
            campaign = campaign,
            dose_center = validated_data['dose_center'],
            first_dose_date = first_dose_date,
            second_dose_date = second_dose_dt,
        )
        return booking

    @staticmethod
    def validate_booking_status(user, current_instance, new_status):
        current_status = current_instance.status if current_instance else None

        if user.is_staff:
            return new_status

        if user.role == 'Patient':
            if new_status not in [BookingDose.BOOKED, BookingDose.CANCELED]:
                raise ValidationError("You can only  booked and canceled the campaign.")
        elif user.role == 'Doctor':
            if not (current_status == BookingDose.BOOKED and new_status == BookingDose.COMPLETED):
                raise ValidationError("Doctors can only set status Booked to 'Completed'.")

        return new_status

