from django.db import models
from users.models import User
from campaigns.models import *

class Center(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField(max_length=100)
    city = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} - {self.city}"

class BookingDose(models.Model):
    BOOKED = 'Booked'
    COMPLETED = 'Completed'
    STATUS_CHOICES = [
        (BOOKED, 'Booked'),
        (COMPLETED, 'Completed'),
    ]

    patient = models.ForeignKey(
        User,on_delete=models.CASCADE
    )
    campaign = models.ForeignKey(
        VaccineCampaign, on_delete=models.CASCADE,related_name='booked'
    )
    dose_center = models.ForeignKey(
        Center, on_delete=models.SET_NULL,related_name='doses', null=True
    )
    first_dose_date = models.DateField()
    second_dose_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,choices=STATUS_CHOICES, default=BOOKED
    )

    def __str__(self):
        return f"{self.patient.username} → {self.campaign.title}"

class VaccinationRecord(models.Model):
    patient = models.ForeignKey(
        User,on_delete=models.CASCADE
    )
    campaign = models.ForeignKey(
        VaccineCampaign, on_delete=models.CASCADE
    )
    dose_number = models.PositiveIntegerField()
    given_date = models.DateField()

    def __str__(self):
        return f"{self.patient.first_name} - Dose {self.dose_number} ({self.campaign.title})"
