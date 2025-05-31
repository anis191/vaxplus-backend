from django.db import models
from users.views import User

# Create your models here.
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
    doctor = models.ForeignKey(
        User,on_delete=models.CASCADE,related_name='campaigns'
    )
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    vaccine_name = models.CharField(max_length=100)
    total_doses = models.PositiveIntegerField(default=2)
    dose_gap = models.PositiveIntegerField(default=30)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='Upcoming')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    rating = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.patient.first_name} on {self.campaign.title}"

