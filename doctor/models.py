from django.db import models

# Create your models here.
from django.conf import settings  # Importing custom user model

 

class DoctorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_profile")
    name = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    experience = models.IntegerField(default=0)
    clinic_address = models.TextField()
    contact_number = models.CharField(max_length=22)
    email = models.EmailField(unique=True)
    availability = models.TextField()  # Example: "Mon-Fri 10 AM - 5 PM"
    about = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to="doctor_profiles/", blank=True, null=True)
    speaks = models.CharField(max_length=50)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)



    def __str__(self):
        return self.name
