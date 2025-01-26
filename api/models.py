from django.db import models
from django.core.validators import MinValueValidator

class Patient(models.Model):
    patientID = models.CharField(max_length=255)
    status = models.CharField(
        max_length=255,
        choices=[
            ('Triaged', 'Triaged'),
            ('Discharged', 'Discharged'),
            ('Admitted', 'Admitted'),
            ('Processing', 'Processing'),
            ('Awaiting Tests', 'Awaiting Tests'),
            ('MIA', 'MIA')
        ],
        default='Triaged'
    )

class Triage(models.Model):
    patientID = models.CharField(max_length=255)
    condition = models.TextField()
    triageCategory = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    present = models.BooleanField(default=True)
    arrivalTime = models.DateTimeField()
    estimatedTreatmentTime = models.IntegerField(validators=[MinValueValidator(1)])
    
    def __str__(self):
        return f"Patient ID: {self.patientID}\nCondition: {self.condition}\nTriage Category: {self.triageCategory}"
    
class Admitted(models.Model):
    patientID = models.CharField(max_length=255)
    physicianID = models.CharField(max_length=255)
    admissionReason = models.TextField()
    ward = models.IntegerField(validators=[MinValueValidator(1)])
    admissionTime = models.DateTimeField()
    
class MissingPatient(models.Model):
    patientID = models.CharField(max_length=255)
    condition = models.TextField()
    triageCategory = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    arrivalTime = models.DateTimeField()
    estimatedTreatmentTime = models.IntegerField(validators=[MinValueValidator(1)])
    
class ProcessPatient(models.Model):
    patientID = models.CharField(max_length=255)
    roomNumber = models.IntegerField(validators=[MinValueValidator(1)])
    triageCategory = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    startTime = models.DateTimeField()
    estimatedEndTime = models.DateTimeField()
    
class Pending(models.Model):
    lab = models.CharField(max_length=255, blank=True, null=True)
    imaging = models.CharField(max_length=255, blank=True, null=True)
    referral = models.CharField(max_length=255, blank=True, null=True)
    
class PendingPatient(models.Model):
    patientID = models.CharField(max_length=255)
    pending = models.ForeignKey(Pending, on_delete=models.CASCADE)