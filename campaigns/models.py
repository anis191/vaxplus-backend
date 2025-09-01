from django.db import models
from users.models import User
# from booking.models import Center
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from datetime import date

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=250,blank=True,null=True)

    def __str__(self):
        return self.name

class Vaccine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500,null=True)
    total_doses = models.PositiveIntegerField(
        default=2,
        validators=[MinValueValidator(1),MaxValueValidator(2)]
    )
    dose_gap = models.PositiveIntegerField(default=30,validators=[MaxValueValidator(365)])
    is_booster = models.BooleanField(default=False)
    booster_gap = models.PositiveIntegerField(
        null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    min_age = models.PositiveIntegerField(null=True)
    max_age = models.PositiveIntegerField(null=True)

    manufacturer = models.CharField(max_length=100, null=True, blank=True)
    approved_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class VaccineCampaign(models.Model):
    UPCOMING = 'Upcoming'
    ONGOING = 'Ongoing'
    PAUSED = 'Paused'
    ENDED = 'Ended'
    CANCELED = 'Canceled'
    STATUS_CHOICES = [
        (UPCOMING, 'Upcoming'),
        (ONGOING, 'Ongoing'),
        (PAUSED, 'Paused'),
        (ENDED, 'Ended'),
        (CANCELED, 'Canceled'),
    ]
    doctor = models.ManyToManyField(
        User,
        related_name='involve_campaigns',
        limit_choices_to={'role': User.DOCTOR}
    )
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,related_name='vaccine_campaigns'
    )
    vaccine = models.ManyToManyField(
        Vaccine,related_name='campaigns',
        limit_choices_to={'is_active': True}
    )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default=UPCOMING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title

class CampaignReview(models.Model):
    patient = models.ForeignKey(
        User,on_delete=models.CASCADE
    )
    campaign = models.ForeignKey(
        VaccineCampaign, on_delete=models.CASCADE, related_name='reviews'
    )
    comment = models.TextField(max_length=200)
    rating = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.patient.first_name} on {self.campaign.title}"


