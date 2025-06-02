from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager
# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    PATIENT = 'Patient'
    DOCTOR = 'Doctor'
    ROLE_CHOICES = [
        (PATIENT, 'Patient'),
        (DOCTOR, 'Doctor'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Patient')
    nid = models.CharField(max_length=20, unique=True)

    USERNAME_FIELD = 'email'  # Use email instead of username
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"

class PatientProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,related_name='patient_profile'
    )
    age = models.PositiveIntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.user.first_name

class DoctorProfile(models.Model):
    user = models.OneToOneField(
        User,on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=50,null=True,blank=True)
    contact = models.CharField(max_length=50,null=True,blank=True)
    profile_picture = models.ImageField(upload_to='doctors/images/', null=True, blank=True)

    def __str__(self):
        return self.user.email