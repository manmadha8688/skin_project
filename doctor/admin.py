from django.contrib import admin
from .models import DoctorProfile


class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "specialization", "experience", "contact_number", "email")
    search_fields = ("name", "specialization", "email")
    list_filter = ("specialization", "experience")

admin.site.register(DoctorProfile,DoctorProfileAdmin)
