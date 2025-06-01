from django.db.models.signals import post_save
from django.dispatch import receiver
from booking.models import BookingDose, VaccinationRecord
from django.db import transaction

@receiver(post_save, sender=BookingDose)
def create_record(sender, instance, created, **kwargs):
    if not created:
        if instance.status == BookingDose.COMPLETED:
            with transaction.atomic():
                if VaccinationRecord.objects.filter(
                    patient = instance.patient,
                    campaign = instance.campaign
                ).exists():
                    return
                
                dates = []
                dates.append(instance.first_dose_date)
                dates.append(instance.second_dose_date)
                records = [
                    VaccinationRecord(
                        patient = instance.patient,
                        campaign = instance.campaign,
                        dose_number = i,
                        given_date = date
                    )
                    for i, date in enumerate(dates, start=1)
                ]
                VaccinationRecord.objects.bulk_create(records)

                instance.delete()