from django.db.models.signals import post_save
from django.dispatch import receiver
from booking.models import BookingDose, VaccinationRecord
from django.db import transaction

@receiver(post_save, sender=BookingDose)
def create_record(sender, instance, created, **kwargs):
    if not created:
        with transaction.atomic():
            dose_number = None
            given_date = None

            if instance.status == BookingDose.FIRST_COMPLETED:
                dose_number = 1
                given_date = instance.first_dose_date
            elif instance.status == BookingDose.SECOND_COMPLETED:
                dose_number = 2
                given_date = instance.second_dose_date
            elif instance.status == BookingDose.COMPLETED:
                if instance.booster_dose_date != None:
                    dose_number = 3
                    given_date = instance.booster_dose_date
                else:
                    dose_number = 2
                    given_date = instance.second_dose_date
            
            if dose_number and given_date:
                VaccinationRecord.objects.create(
                    patient = instance.patient,
                    campaign = instance.campaign,
                    vaccine = instance.vaccine,
                    dose_number = dose_number,
                    given_date = given_date
                )

            if instance.status == BookingDose.COMPLETED:
                instance.delete()
