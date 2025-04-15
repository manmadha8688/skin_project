from django.urls import path
from . import views

app_name= 'review'

urlpatterns = [
    path('add_review',views.add_review,name='add_review'),
]
