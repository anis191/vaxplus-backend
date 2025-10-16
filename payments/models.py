from django.db import models
from users.models import User
from campaigns.models import VaccineCampaign

class Payment(models.Model):
    PENDING = 'Pending'
    SUCCESS = 'Success'
    FAILED = 'Failed'
    REFUNDED = 'Refunded'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
        (REFUNDED, 'Refunded'),
    ]
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="campaign_registrations")
    campaign = models.ForeignKey(VaccineCampaign, on_delete=models.SET_NULL, related_name="registrations",null=True,blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    is_donate = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.is_donate:
            return f"{self.patient.first_name} {self.patient.last_name} - Donate at ({self.created_at})"
        return f"{self.patient.first_name} {self.patient.last_name} - Pay at ({self.created_at})"
