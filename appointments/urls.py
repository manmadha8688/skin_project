from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.booking,name='appointments'),
    path('my-appointments',views.patient_appointments,name='my-appointments'),
    path('book_appointment',views.book_appointment,name='book_appointment'),
    path('update-doctor-appointment-status/<int:appointment_id>/', views.update_appointment_status, name='update-doctor-appointment-status'),
    
    
   
]
