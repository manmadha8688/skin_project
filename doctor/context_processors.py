from .models import DoctorProfile  # Import your Doctor model

def doctor_profile(request):
    if request.user.is_authenticated:
        try:
            doctor =request.user.doctor_profile # Fetch doctor profile
        except DoctorProfile.DoesNotExist:
            doctor = None  # If the user is not a doctor
    else:
        doctor = None  # If the user is not logged in

    return {'doctor': doctor}  # Available in all templates
