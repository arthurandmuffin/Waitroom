from django.urls import path
from . import views

urlpatterns = [
    path('add-patient/', views.create_triage, name='add_patient'),
    path('admit-patient/', views.admit_patient, name='admit_patient'),
    path('missing-patient/', views.missing_patient, name='missing_patient'),
    path('remove-patient/', views.remove_patient, name='remove_patient')
]
