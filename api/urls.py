from django.urls import path
from . import views

urlpatterns = [
    path('add-patient/', views.create_triaige, name='add_patient'),
]
