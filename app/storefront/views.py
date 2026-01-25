from django.shortcuts import render
from django.db import transaction
from .models import Activity, Participant, Tema
from .serializers import ActivitySerializer, ParticipantSerializer, TemaSerializer
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework import status


class ParticipantListPagination(PageNumberPagination):
    """Custom pagination for participant list with max page size of 10."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10
    
    def paginate_queryset(self, queryset, request, view=None):
        """Store the queryset to calculate active/inactive counts."""
        self.queryset = queryset
        return super().paginate_queryset(queryset, request, view)
    
    def get_paginated_response(self, data):
        """Add active and inactive participant counts to the response."""
        # Calculate counts from the filtered queryset
        total_count = self.queryset.count()
        active_count = self.queryset.filter(is_active=True).count()
        inactive_count = self.queryset.filter(is_active=False).count()
        
        return Response({
            'count': self.page.paginator.count,
            'total_active': active_count,
            'total_inactive': inactive_count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

class TemaViewSet(viewsets.ModelViewSet):
    queryset = Tema.objects.order_by('id')
    serializer_class = TemaSerializer
    
    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.order_by('id')
    serializer_class = ActivitySerializer
    
    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]


class ParticipantViewSet(viewsets.ModelViewSet):
    """
    List participants with filtering by name, last_name, dni, celphone, and email.
    Supports pagination with max page size of 10.
    
    Query parameters:
    - name: Filter by name (partial match, case-insensitive)
    - last_name: Filter by last name (partial match, case-insensitive)
    - dni: Filter by DNI (partial match, case-insensitive)
    - celphone: Filter by cellphone (partial match, case-insensitive)
    - email: Filter by email (partial match, case-insensitive)
    - page: Page number for pagination
    - page_size: Items per page (max 10)
    """
    queryset = Participant.objects.all().order_by('-created_at')
    serializer_class = ParticipantSerializer
    pagination_class = ParticipantListPagination
    
    # def get_permissions(self):
    #     if self.request.method == 'POST':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Get filter parameters
        name = self.request.query_params.get('name', None)
        last_name = self.request.query_params.get('last_name', None)
        dni = self.request.query_params.get('dni', None)
        celphone = self.request.query_params.get('celphone', None)
        email = self.request.query_params.get('email', None)
        
        # Apply filters (case-insensitive partial matching)
        if name:
            queryset = queryset.filter(name__icontains=name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if dni:
            queryset = queryset.filter(dni__icontains=dni)
        if celphone:
            queryset = queryset.filter(celphone__icontains=celphone)
        if email:
            queryset = queryset.filter(email__icontains=email)
        
        return queryset

    @action(detail=False, methods=['get'])
    def by_dni(self, request):
        dni = request.query_params.get('dni', None)
        if dni:
            try:
                participant = Participant.objects.get(dni=dni)
                return Response(ParticipantSerializer(participant).data)
            except Participant.DoesNotExist:
                # return empty obj and 200 status
                return Response({}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def update_activity_by_qr(self, request):
        """
        Update participant activities by QR code.
        
        Expected POST data:
        {
            "qr": "participant_qr_code",
            "activity_id": 1
        }
        """
        qr = request.data.get('qr', None)
        activity_id = request.data.get('activity_id', None)
        
        # Validate required fields
        if not qr:
            return Response(
                {'error': 'El QR es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not activity_id:
            return Response(
                {'error': 'El ID de la actividad es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Wrap all database operations in an atomic transaction
        try:
            with transaction.atomic():
                # Find participant by QR code
                try:
                    participant = Participant.objects.select_for_update().get(qr_code=qr)
                except Participant.DoesNotExist:
                    return Response(
                        {'error': 'No se encontró el participante con el QR proporcionado'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                # Get the activity
                try:
                    activity = Activity.objects.select_for_update().get(id=activity_id, is_active=True)
                except Activity.DoesNotExist:
                    return Response(
                        {'error': 'No se encontró la actividad'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                # Check if activity is already in participant's activities
                if participant.activities.filter(id=activity_id).exists():
                    return Response(
                        {
                            'error': 'La actividad ya ha sido registrada para este participante',
                            'participant': ParticipantSerializer(participant).data
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Add activity to participant
                participant.activities.add(activity)
                
                # Refresh participant to get updated activities
                participant.refresh_from_db()
                
                # Return updated participant data
                serializer = ParticipantSerializer(participant)
                return Response({
                    'message': 'Actividad registrada correctamente',
                    'participant': serializer.data
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response(
                {'error': f'Error al registrar la actividad: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
