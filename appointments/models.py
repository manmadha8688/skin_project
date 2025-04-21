from django.db import models
from doctor.models import DoctorProfile
from django.conf import settings
from django.db import models
from app.models import PatientProfile

class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Cancelled", "Cancelled"),
    ] 

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="doctor_requests")
 
    patient_name = models.CharField(max_length=255)
    patient_gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],blank=True)
    patient_age = models.PositiveIntegerField(blank=True)
    patient_email = models.EmailField(blank=True,)
    patient_number = models.CharField(max_length=15,blank=True,)
    
    disease = models.CharField(max_length=255, blank=True, null=True)
    confidence = models.CharField(max_length=50, blank=True, null=True)
    severity = models.CharField(max_length=50, blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    addittional_information = models.TextField(blank=True, null=True)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    image = models.ImageField(upload_to='appointment_images/', blank=True, null=True)
    



    def __str__(self):
        return f"Appointment with {self.doctor} on {self.date}"
