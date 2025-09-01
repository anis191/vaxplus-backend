from django.db import models
from users.models import User
from campaigns.models import *
from uuid import uuid4

class Center(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=100)
    city = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} - {self.city}"

class BookingDose(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    BOOKED = 'Booked'
    FIRST_COMPLETED = 'FirstCompleted'
    SECOND_COMPLETED = 'SecondCompleted'
    COMPLETED = 'Completed'
    CANCELED = 'Canceled'
    STATUS_CHOICES = [
        (BOOKED, 'Booked'),
        (FIRST_COMPLETED, 'First Dose Completed'),
        (SECOND_COMPLETED, 'Second Dose Completed'),
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'), 
    ]

    patient = models.ForeignKey(
        User,on_delete=models.CASCADE
    )
    campaign = models.ForeignKey(
        VaccineCampaign, on_delete=models.CASCADE,related_name='booked'
    )
    vaccine = models.ForeignKey(
        Vaccine, on_delete=models.CASCADE,related_name='booked_vaccine'
    )
    dose_center = models.ForeignKey(
        Center, on_delete=models.SET_NULL,related_name='doses', null=True
    )
    first_dose_date = models.DateField()
    second_dose_date = models.DateField(null=True, blank=True)
    booster_dose_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,choices=STATUS_CHOICES, default=BOOKED
    )

    def __str__(self):
        return f"{self.patient.first_name} → {self.campaign.title}"

class VaccinationRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    patient = models.ForeignKey(
        User,on_delete=models.CASCADE
    )
    campaign = models.ForeignKey(
        VaccineCampaign, on_delete=models.CASCADE
    )
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE,related_name='completed_vaccine')
    dose_number = models.PositiveIntegerField()
    given_date = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['patient', 'campaign', 'vaccine', 'dose_number'],
                name='unique_vaccination_record'
            )
        ]
        ordering = ['given_date']

    def __str__(self):
        return f"{self.patient.first_name} - Dose {self.dose_number} ({self.vaccine.name}-{self.campaign.title})"
    
