from django.contrib import admin
from .models import Patient, Triage, Admitted, MissingPatient, ProcessPatient, Pending, PendingPatient

admin.site.register(Patient)
admin.site.register(Triage)
admin.site.register(Admitted)
admin.site.register(MissingPatient)
admin.site.register(ProcessPatient)
admin.site.register(Pending)
admin.site.register(PendingPatient)