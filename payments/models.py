from django.db import models
from users.models import User

class Payment(models.Model):
    PENDING = 'Pending'
    SUCCESS = 'Success'
    CANCELLED = 'Cancelled'
    REFUNDED = 'Refunded'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SUCCESS, 'Success'),
        (CANCELLED, 'Cancelled'),
        (REFUNDED, 'Refunded'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - Pay at ({self.created_at})"
