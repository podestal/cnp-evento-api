from django.shortcuts import render
from .models import Activity, Participant
from .serializers import ActivitySerializer, ParticipantSerializer
from rest_framework import viewsets

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
