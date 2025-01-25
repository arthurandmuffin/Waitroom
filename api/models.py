from django.db import models
from django.core.validators import MinValueValidator

class Triage(models.Model):
    patientID = models.CharField(max_length=255)
    condition = models.TextField()
    triageCategory = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    arrivalTime = models.DateTimeField()
    estimatedTreatmentTime = models.IntegerField(validators=[MinValueValidator(1)])
    
    def __str__(self):
        return f"Patient ID: {self.patientID}\nCondition: {self.condition}\nTriage Category: {self.triageCategory}"