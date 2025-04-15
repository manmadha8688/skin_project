from .models import PatientProfile  # Import your Doctor model

def patient_profile(request):
    if request.user.is_authenticated:
        try:
            patient = PatientProfile.objects.get(user=request.user)  # Fetch doctor profile
        except PatientProfile.DoesNotExist:
            patient = None  # If the user is not a doctor
    else:
        patient = None  # If the user is not logged in

    return {'patient': patient}  # Available in all templates
