from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Triage
from .serializers import TriageSerializer

@api_view(['POST'])
def create_triaige(request):
    if request.method == 'POST':
        data = request.data
        data['arrivalTime'] = timezone.now()
        
        serializer = TriageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)