from datetime import timedelta, date, datetime
from campaigns.models import *
from booking.models import *
from payments.models import Payment
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
        vaccine = validated_data['vaccine']

        if campaign.is_premium:
            if not Payment.objects.filter(patient=user, campaign=campaign, status=Payment.SUCCESS).exists():
                raise ValidationError("This is a premium vaccine campaign. Please complete payment before booking.")

        if BookingDose.objects.filter(patient=user, campaign=campaign, vaccine=vaccine).exists():
            raise ValidationError("You have already booked this vaccine in this campaign. Please check your bookings.")
        
        if VaccinationRecord.objects.filter(patient=user, campaign=campaign, vaccine=vaccine).exists():
            raise ValidationError("You have already completed doses for this vaccine in this campaign.")
        
        # Age check:
        if user.patient_profile.date_of_birth is None or (user.patient_profile.blood_group == "" or user.patient_profile.blood_group is None):
            raise ValidationError("Please update your patient profile with date of birth and blood group before booking.")
        elif not (vaccine.min_age <= user.patient_profile.age <= vaccine.max_age):
            raise ValidationError(f"This vaccine is allowed for ages {vaccine.min_age} to {vaccine.max_age}. Your age does not match.")

        first_dose_dt = validated_data.pop('dates')
        first_dose_date = datetime.strptime(first_dose_dt, '%Y-%m-%d').date()
        gap = vaccine.dose_gap
        second_dose_dt = first_dose_date + timedelta(days=gap)
        
        booster_dose_date = None
        if vaccine.is_booster:
            if not vaccine.booster_gap:
                raise ValidationError("Booster_gap is missing.")
            booster_dose_date = second_dose_dt + timedelta(days=vaccine.booster_gap)

        status = campaign.status
        if status in ['Ended','Paused','Canceled']:
            raise ValidationError("This campaign is not active.")
        elif date.today() > campaign.end_date:
            raise ValidationError("Campaign already ended.")
        
        booking = BookingDose.objects.create(
            patient = user,
            campaign = campaign,
            vaccine = vaccine,
            dose_center = validated_data['dose_center'],
            first_dose_date = first_dose_date,
            second_dose_date = second_dose_dt,
            booster_dose_date = booster_dose_date
        )
        return booking

    @staticmethod
    def validate_booking_status(user, current_instance, new_status):
        current_status = current_instance.status if current_instance else None
        booster_dose_ck = current_instance.booster_dose_date if current_instance else None

        if user.is_staff:
            return new_status

        if user.role == 'Patient':
            if new_status not in [BookingDose.BOOKED, BookingDose.CANCELED]:
                raise ValidationError("You can only cancel the booking.")
            if new_status == BookingDose.CANCELED and current_status != BookingDose.BOOKED:
                raise ValidationError(f"Your booking is already '{current_status}'. You cannot cancel it now.")
        elif user.role == 'Doctor':
            if current_status == BookingDose.BOOKED:
                if new_status != BookingDose.FIRST_COMPLETED:
                    raise ValidationError("Next allowed status is 'First Dose Completed'.")
            elif current_status == BookingDose.FIRST_COMPLETED:
                if booster_dose_ck:
                    if new_status != BookingDose.SECOND_COMPLETED:
                        raise ValidationError("Next allowed status is 'Second Dose Completed' before marking booster.")
                else:
                    if new_status != BookingDose.COMPLETED:
                        raise ValidationError("No booster scheduled. You can directly mark 'Completed'.")
            elif current_status == BookingDose.SECOND_COMPLETED:
                if booster_dose_ck:
                    if new_status != BookingDose.COMPLETED:
                        raise ValidationError("After second dose, next allowed status is 'Completed'.")
            else:
                raise ValidationError("Invalid status update.")

        return new_status

