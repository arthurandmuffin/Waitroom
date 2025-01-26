from rest_framework import serializers
from .models import Patient, Triage, Admitted, MissingPatient, Pending, PendingPatient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['patientID', 'status']

class TriageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Triage
        fields = ['patientID', 'condition', 'triageCategory', 'arrivalTime', 'estimatedTreatmentTime']
        
class AdmittedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admitted
        fields = ['patientID', 'physicianID', 'admissionReason', 'ward', 'admissionTime']
        
class MissingPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingPatient
        fields = ['patientID', 'condition', 'triageCategory', 'arrivalTime', 'estimatedTreatmentTime']
        
class PendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pending
        fields = ['lab', 'imaging', 'referral']
        
class PendingPatientSerializer(serializers.ModelSerializer):
    pending = PendingSerializer()  # This will serialize the nested 'status' object

    class Meta:
        model = PendingPatient
        fields = ['patientID', 'pending']
