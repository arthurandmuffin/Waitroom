from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('check-in/', views.check_patient_in, name='check_patient_in'),  # Check-in page
]