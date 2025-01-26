from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Patient, Triage, Admitted, MissingPatient, ProcessPatient, Pending, PendingPatient
from .serializers import PatientSerializer, TriageSerializer, AdmittedSerializer, MissingPatientSerializer, ProcessPatientSerializer ,PendingSerializer, PendingPatientSerializer
from datetime import timedelta
from .signals import TriagesToNotify

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
def patient_check_in(request):
    if request.method == 'POST':
        data = request.data
        patientID = data['patientID']
        try:
            triage = Triage.objects.get(patientID=patientID)
            triage.present = True
        except Triage.DoesNotExist:
            return Response({"error": "Triage record not found."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_200_OK)
    
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
            triage = Triage.objects.get(patientID=patientID)
            serializer = MissingPatientSerializer(data=TriageSerializer(triage).data)
            triage.delete()
        except Patient.DoesNotExist:
            return Response({"error": "Patient record not found."}, status=status.HTTP_401_UNAUTHORIZED)
        except Triage.DoesNotExist:
            return Response({"error": "Triage record not found."}, status=status.HTTP_401_UNAUTHORIZED)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def process_patient(request):
    if request.method == 'POST':
        data = request.data
        patientID = data['patientID']
        if patientID == None:
            return Response({"error": "Missing patientID."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            patient = Patient.objects.get(patientID=patientID)
            triage = Triage.objects.get(patientID=patientID)
            patient.status = "Processing"
            estimatedTime = triage.estimatedTreatmentTime
            ProcessPatient.objects.create(
                patientID=patientID,
                roomNumber=data['roomNumber'],
                triageCategory=triage.triageCategory,
                startTime=timezone.now(),
                estimatedEndTime=timezone.now() + timedelta(minutes=estimatedTime)
            )
            patient.save()
            triage.delete()
        except Patient.DoesNotExist:
            return Response({"error": "Patient record not found."}, status=status.HTTP_401_UNAUTHORIZED)
        except Triage.DoesNotExist:
            return Response({"error": "Triage record not found."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_201_CREATED)
    
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
                processPatient = ProcessPatient.objects.get(patientID=patientID)
                processPatient.delete()
            except ProcessPatient.DoesNotExist:
                return Response({"error": "ProcessPatient record not found."}, status=status.HTTP_401_UNAUTHORIZED)
            except Patient.DoesNotExist:
                return Response({"error": "Patient record not found."}, status=status.HTTP_401_UNAUTHORIZED)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def discharge_patient(request):
    if request.method == 'POST':
        data = request.data
        patientID = data['patientID']
        if patientID == None:
            return Response({"error": "Missing patientID."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            patient = Patient.objects.get(patientID=patientID)
            patient.status = "Discharged"
            patient.save()
            processPatient = ProcessPatient.objects.get(patientID=patientID)
            processPatient.delete()
        except Patient.DoesNotExist:
            return Response({"error": "Patient record not found."}, status=status.HTTP_401_UNAUTHORIZED)
        except ProcessPatient.DoesNotExist:
            return Response({"error": "ProcessPatient record not found."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_200_OK)
    
@api_view(['POST'])
def pending_patient(request):
    if request.method == 'POST':
        data = request.data
        patientID = data['patientID']
        if patientID == None:
            return Response({"error": "Missing patientID."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PendingPatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def test_ready_patient(request):
    if request.method == 'POST':
        data = request.data
        patientID = data['patientID']
        if patientID == None:
            return Response({"error": "Missing patientID."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            pendingPatient = PendingPatient.objects.get(patientID=patientID)
            processedPatient = ProcessPatient.objects.get(patientID=patientID)
            Triage.objects.create(
                patientID=patientID,
                condition="View test results",
                triageCategory=processedPatient.triageCategory,
                arrivalTime = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0),
                estimatedTreatmentTime = 5
            )
            pendingPatient.delete()
            processedPatient.delete()

        except PendingPatient.DoesNotExist:
            return Response({"error": "PendingPatient record not found."}, status=status.HTTP_401_UNAUTHORIZED)
        except ProcessPatient.DoesNotExist:
            return Response({"error": "ProcessPatient record not found."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
def all_active_triages(request):
    try:
        activeTriages = Triage.objects.order_by('triageCategory', 'arrivalTime')
        serializer = TriageSerializer(activeTriages, many=True)
        return Response(serializer.data)
    except Triage.DoesNotExist:
        return Response(None)

@api_view(['GET'])
def all_present_triages(request):
    try:
        presentTriages = Triage.objects.filter(present=True).order_by('triageCategory', 'arrivalTime')
        serializer = TriageSerializer(presentTriages, many=True)
        return Response(serializer.data)
    except Triage.DoesNotExist:
        return Response(None)

@api_view(['GET'])
def all_processing_patients(request):
    try:
        processingPatients = ProcessPatient.objects.order_by('roomNumber')
        serializer = ProcessPatientSerializer(processingPatients, many=True)
        return Response(serializer.data)
    except ProcessPatient.DoesNotExist:
        return Response(None)
    
@api_view(['GET'])
def patients_to_notify(request):
    try:
        patientsToNotify = TriagesToNotify()
        serializer = TriageSerializer(patientsToNotify)
        return Response(serializer.data)
    except Triage.DoesNotExist:
        return Response(None)