from rest_framework import serializers
from .models import Patient, Triage, Admitted, MissingPatient, ProcessPatient, Pending, PendingPatient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['patientID', 'status']

class TriageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Triage
        fields = ['patientID', 'condition', 'triageCategory', 'present', 'arrivalTime', 'estimatedTreatmentTime']
        
class AdmittedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admitted
        fields = ['patientID', 'physicianID', 'admissionReason', 'ward', 'admissionTime']
        
class MissingPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingPatient
        fields = ['patientID', 'condition', 'triageCategory', 'arrivalTime', 'estimatedTreatmentTime']
        
class ProcessPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessPatient
        fields = ['patientID', 'roomNumber', 'triageCategory', 'startTime', 'estimatedEndTime']
        
class PendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pending
        fields = ['lab', 'imaging', 'referral']
        
class PendingPatientSerializer(serializers.ModelSerializer):
    pending = PendingSerializer()
    class Meta:
        model = PendingPatient
        fields = ['patientID', 'pending']
        
    def create(self, validated_data):
        pending_data = validated_data.pop('pending')
        pending_instance = Pending.objects.create(**pending_data)
        pending_patient = PendingPatient.objects.create(pending=pending_instance, **validated_data)
        return pending_patient
