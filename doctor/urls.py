from django.urls import path
from . import views

urlpatterns = [
    
  path('',views.dashboard,name="doctor"),
  path('dashboard',views.dashboard,name="dashboard"),
  path('myprofile',views.myprofile,name="myprofile"), 
  path('update-profile/',views.update_profile,name="update-profile"),
  path("save-location/", views.save_location, name="save-location"),
  path('appointment-request',views.appointment_request,name="appointment-request"),  
  path('accepted-appointments/',views.accepted_appointments,name="accepted-appointments"),
  path('update-patient-appointment/<int:appointment_id>/', views.update_appointment_status, name='update-patient-appointment-status'),
  path('cancell-patient-appointment/<int:appointment_id>/', views.cancell_patient_appointment, name='cancell-patient-appointment'),

 
    
] 