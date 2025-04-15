from django.shortcuts import render,redirect
from .models import DoctorProfile
from appointments.models import Appointment
from django.contrib import messages
# Create your views here.
def dashboard(request):
    doctor = DoctorProfile.objects.get(user=request.user)
    appointment = Appointment.objects.filter(doctor=doctor)
    
    return render(request,'doctor/dashboard.html', {'appointments':appointment})


def myprofile(request):
    
    try:
        doctor = DoctorProfile.objects.get(user=request.user)
    except DoctorProfile.DoesNotExist:
        doctor = None  # No profile exists yet

    if request.method == "POST":
        if doctor is None:
            doctor = DoctorProfile(user=request.user)

        # Update profile fields
        doctor.name = request.POST.get("name")
        doctor.qualification = request.POST.get("qualification")
        doctor.specialization = request.POST.get("specialization")
        doctor.experience = request.POST.get("experience")
        doctor.contact_number = request.POST.get("contact_number")
        doctor.email = request.POST.get("email")
        doctor.availability = request.POST.get("availability")
        doctor.about = request.POST.get("about")
        doctor.speaks = request.POST.get("speaks")

        doctor.save()
        return redirect('myprofile')
        
  # Redirect to refresh profile view

    return render(request,'doctor/my-profile.html', {"doctor": doctor})

def update_profile(request):
    if request.method == "POST" and request.FILES.get("profile_image"):
        try:

            doctor = DoctorProfile.objects.get(user=request.user)
            doctor.profile_image = request.FILES["profile_image"] 
            doctor.save()
        except DoctorProfile.DoesNotExist:
            messages.error(request,"Save Yours Details first then after change  profile ")
         

    return redirect("myprofile")
def save_location(request):

    if request.method == "POST":
        lat = request.POST.get("latitude")
        lon = request.POST.get("longitude")
        address = request.POST.get("address")


        if lat and lon and address:
            doctor = DoctorProfile.objects.filter(user=request.user).first()

            if doctor:
                doctor.latitude = float(lat)
                doctor.longitude = float(lon)
                doctor.address = address
                doctor.save() 
                return redirect("myprofile")
            else:
                print("Error: Doctor profile not found!")

    
    return redirect("myprofile")

def accepted_appointments(request):
    try:
        doctor = DoctorProfile.objects.get(user=request.user)
    except DoctorProfile.DoesNotExist:
        messages.error(request,'Enter details to get Appointments')
        return redirect('myprofile')
    appointments = Appointment.objects.filter(doctor=doctor,status="Approved")
    return render(request,'doctor/accepted-appointments.html',{'appointments':appointments})

def appointment_request(request):
    try:
        doctor = DoctorProfile.objects.get(user=request.user)
        appointments = Appointment.objects.filter(doctor=doctor,status="Pending")
    except DoctorProfile.DoesNotExist:
        messages.error(request,'Enter details to get Appointments')
        return redirect('myprofile')
    return render(request,'doctor/appointment-request.html',{'appointments':appointments})

def update_appointment_status(request, appointment_id):
    if request.method == "POST":
        new_status = request.POST.get("status") 
        print(new_status+"status")
        
        if new_status not in ["Approved", "Rejected","Cancelled"]:
            return redirect("appointment-request")  # Redirect back if invalid

        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = new_status
        appointment.save()

        return redirect("appointment-request") 
    
def cancell_patient_appointment(request,appointment_id):
    if request.method == "POST":
        new_status = request.POST.get("status") 
        print(new_status+"status")
        
        if new_status not in ["Approved", "Rejected","Cancelled"]:
            return redirect("appointment-request")  # Redirect back if invalid

        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = new_status
        appointment.save()

        return redirect("accepted-appointments") 
    