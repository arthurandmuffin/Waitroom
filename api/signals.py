from django.db.models.signals import post_save, post_delete
from django.db.models import Sum
from django.dispatch import receiver
from .models import Triage
from ..Waitroom.env import WaitingRoomBuffer

@receiver(post_save, sender=Triage)
def newTriage(sender, instance, created, **kwargs):
    presentTriages = Triage.objects.filter(present=True).order_by('triageCategory', 'arrivalTime')
    totalTreatmentTime = presentTriages.aggregate(Sum('estimatedTreatmentTime'))['estimatedTreatmentTime__sum']
    totalTreatmentTime = totalTreatmentTime or 0
    
    nonpresentTriages = Triage.objects.filter(present=False).order_by('triageCategory', 'arrivalTime')
    triagesToNotify = []
    if totalTreatmentTime < WaitingRoomBuffer and nonpresentTriages.exists():
        highestPriority = nonpresentTriages.first()
        triagesToNotify.append(highestPriority)
    #Have list of patient to notify, connect to hospital SMS infrastructure
    