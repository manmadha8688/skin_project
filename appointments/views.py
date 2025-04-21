from django.shortcuts import render
from doctor.models import DoctorProfile
from app.models import PatientProfile
from geopy.distance import geodesic 
# Create your views here.
def booking(request):
    experience = request.POST.get('experience', '')
    language = request.POST.get("language", "")
    user_lat = request.POST.get("latitude", "")
    user_lon = request.POST.get("longitude", "")
    

    doctors = DoctorProfile.objects.all()

        # Filter by Experience
    if experience:
        doctors = doctors.filter(experience__gte=int(experience))

        # Filter by Language
    if language:
        doctors = doctors.filter(speaks__icontains=language)
    total = doctors.count()

        # Filter by Location (within 50km radius)
    if user_lat and user_lon:
        user_location = (float(user_lat), float(user_lon))
        filtered_doctors = []
            
        for doctor in doctors:
            doctor_location =  (float(doctor.latitude), float(doctor.longitude)) # Ensure these fields exist
            distance = geodesic(user_location, doctor_location).km  # Calculate distance
            print(user_location)
            print(doctor_location)
            print(distance)
            if distance <= 50:  # Doctors within 50km
                filtered_doctors.append(doctor)
        
        doctors = filtered_doctors
    doctor = [
        {'name': f'Doctor {i}', 'qualification': 'MBBS, MD', 'specialization': 'Dermatology', 'experience': 10 + i, 'speaks': 'English, Hindi', 'availability': 'Mon-Fri, 9 AM - 5 PM', 'address': f'Clinic {i} St.', 'contact_number': f'123-456-78{i}0', 'email': f'doctor{i}@example.com', 'profile_image': 'doctor-demo.jpeg'}
        for i in range(1, 11)
        ]
    doctors = list(doctors) + doctor
    
    return render(request,'appointment/booking-appointment.html',{'doctors':doctors,"total":total})



from django.shortcuts import render, redirect,get_list_or_404
from django.contrib import messages
from .models import Appointment
import base64
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
def book_appointment(request):

    

    if request.method == "POST":
        if "reset" in request.POST:  # If reset button was clicked
            request.session.flush()  # Clears the entire session
            return redirect('book_appointment') 
        
        doctor_id = int(request.POST.get("doctor"))
        patient_name = request.POST.get("patient_name")
        patient_number = request.POST.get("patient_number")
        patient_gender = request.POST.get("patient_gender")
        patient_age = request.POST.get("patient_age")
        patient_email = request.POST.get("patient_email")
        disease = request.POST.get("disease", "Not Provided")
        confidence = request.POST.get("confidence", "N/A")
        severity = request.POST.get("severity", "N/A")
        symptoms = request.POST.get("symptoms", "N/A")
        message = request.POST.get("message", "N/A")
        date = request.POST.get("date")

        # Save to database 
        doctor = DoctorProfile.objects.get(id=doctor_id)

        patient = PatientProfile.objects.get(user=request.user)
        appointment = Appointment.objects.create(
            doctor=doctor,
            patient=patient,
            patient_name=patient_name,
            patient_age=patient_age,
            patient_gender = patient_gender,
            patient_number = patient_number,
            patient_email = patient_email,
            disease=disease,
            confidence=f"{float(confidence):.2f}",
            severity=severity,
            symptoms=symptoms,
            addittional_information=message,
            date=date,
            status="Pending"  # Default status
        )
        if "uploaded_image" in request.session:
                img_data = base64.b64decode(request.session["uploaded_image"])
                appointment.image.save("appointment_image.jpg", ContentFile(img_data), save=True)
                request.session.pop("uploaded_image", None) 

        elif 'image' in request.FILES:
            # ✅ If no session image, save uploaded image
            uploaded_image = request.FILES['image']
            appointment.image = uploaded_image
        appointment.save()
        
    session_keys = ["predicted_class", "confidence", "severity", "symptoms"]
    for key in session_keys:
        request.session.pop(key, None)  # Removes key if it exists

        
    return redirect('my-appointments')

def patient_appointments(request):
    patient = PatientProfile.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient=patient)
   
    return render(request,'appointment/my-appointments.html',{'appointments':appointments})

def update_appointment_status(request, appointment_id):
    if request.method == "POST":
        new_status = request.POST.get("status") 
        
        if new_status not in ["Approved", "Rejected","Cancelled"]:
            return redirect("my-appointments")  # Redirect back if invalid

        appointment = Appointment.objects.get(id=appointment_id)
        appointment.status = new_status
        appointment.save()

        return redirect("my-appointments") 
    
