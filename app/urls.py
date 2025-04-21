from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('patient/',views.patient,name='patient'),
    path('profile',views.profile,name="profile"),
    path('update_profile/',views.update_profile,name="update_profile"),
    

]
