from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Patient, Triage, Admitted, MissingPatient
from .serializers import PatientSerializer, TriageSerializer, AdmittedSerializer, MissingPatientSerializer

@api_view(['POST'])
def create_triage(request):
    if request.method == 'POST':
        data = request.data
        data['arrivalTime'] = timezone.now()
        
        patientID = data['patientID']
        try:
            patient = Patient.objects.get(patientID=patientID)
        except Patient.DoesNotExist:
            Patient.objects.create(
                patientID=patientID,
                status='Triaged'
            )
        
        serializer = TriageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def admit_patient(request):
    if request.method == 'POST':
        data = request.data
        data['admissionTime'] = timezone.now()
        
        serializer = AdmittedSerializer(data=data)
        
        if serializer.is_valid():
            try:
                patientID=data['patientID']
                patient = Patient.objects.get(patientID=patientID)
                patient.status = "Admitted"
                patient.save()
                triage = Triage.objects.get(patientID=patientID)
                triage.delete()
            except Triage.DoesNotExist:
                return Response({"error": "Triage record not found."}, status=status.HTTP_401_UNAUTHORIZED)
            except Patient.DoesNotExist:
                return Response({"error": "Patient record not found."}, status=status.HTTP_401_UNAUTHORIZED)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def missing_patient(request):
    if request.method == 'POST':
        data = request.data
        patientID = data['patientID']
        if patientID == None:
            return Response({"error": "Missing patientID."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            patient = Patient.objects.get(patientID=patientID)
            patient.status = "MIA"
            patient.save()
            serializer = MissingPatientSerializer(data=TriageSerializer(Triage.objects.get(patientID=patientID)).data)
        except Patient.DoesNotExist:
            return Response({"error": "Patient record not found."}, status=status.HTTP_401_UNAUTHORIZED)
        except Triage.DoesNotExist:
            return Response({"error": "Triage record not found."}, status=status.HTTP_401_UNAUTHORIZED)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def remove_patient(request):
    if request.method == 'POST':
        data = request.data
        patientID = data['patientID']
        if patientID == None:
            return Response({"error": "Missing patientID."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            patient = Patient.objects.get(patientID=patientID)
            patient.status = "Discharged"
            patient.save()
            triage = Triage.objects.get(patientID=patientID)
            triage.delete()
        except Patient.DoesNotExist:
            return Response({"error": "Patient record not found."}, status=status.HTTP_401_UNAUTHORIZED)
        except Triage.DoesNotExist:
            return Response({"error": "Triage record not found."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_200_OK)