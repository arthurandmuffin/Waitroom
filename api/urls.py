from django.urls import path
from . import views

urlpatterns = [
    path('add-patient/', views.create_triage, name='add_patient'),
    path('patient-check-in/', views.patient_check_in, name='patient_check_in'),
    path('missing-patient/', views.missing_patient, name='missing_patient'),
    path('process-patient/', views.process_patient, name='process_patient'),
    path('admit-patient/', views.admit_patient, name='admit_patient'),
    path('discharge-patient/', views.discharge_patient, name='discharge_patient'),
    path('pending-patient/', views.pending_patient, name='pending_patient'),
    path('test-ready-patient/', views.test_ready_patient, name='test_ready_patient'),
    
    path('all-active-triages')
]
