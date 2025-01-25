from rest_framework import serializers
from .models import Triage

class TriageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Triage
        fields = ['patientID', 'condition', 'triageCategory', 'arrivalTime', 'estimatedTreatmentTime']