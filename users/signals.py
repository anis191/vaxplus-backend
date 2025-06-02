from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User, PatientProfile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.PATIENT:
        PatientProfile.objects.create(
            user = instance
        )
