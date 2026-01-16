from django.shortcuts import render
from .models import Activity, Participant, Tema
from .serializers import ActivitySerializer, ParticipantSerializer, TemaSerializer
from rest_framework import viewsets


class TemaViewSet(viewsets.ModelViewSet):
    queryset = Tema.objects.order_by('id')
    serializer_class = TemaSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
