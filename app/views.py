from django.shortcuts import render,redirect
from django.contrib.auth.models import auth,User
from review.models import reviews
from datetime import datetime

def patient(request):   
    r =reviews.objects.all()
    return render(request,'home-page/index.html',{'reviews':r})

def index(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'doctor_profile'):  # Check if user is a doctor
            return redirect('doctor')
    
        return redirect('patient')  # Redirect normal users
    r =reviews.objects.all()
    return render(request,'home-page/index.html',{'reviews':r})
from .models import PatientProfile

def profile(request):
    profile, created = PatientProfile.objects.get_or_create(user=request.user)
    

    if request.method == 'POST':
        
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        
        date_of_birth = request.POST.get('date_of_birth')
        if date_of_birth:
            try:
                dob = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
            except ValueError:
                dob = None
        else:
            dob = None
        profile.date_of_birth = dob
        profile.age = int(request.POST.get('age', profile.age))
        
        profile.gender = request.POST.get('gender', profile.gender)

        
        profile.save()
        

    return render(request, 'patient/profile.html', {'patient': profile})
def update_profile(request):
    profile, created = PatientProfile.objects.get_or_create(user=request.user)
    
    if request.method == "POST" and 'profile_picture' in request.FILES:
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
    return render(request, 'patient/profile.html', {'patient': profile})