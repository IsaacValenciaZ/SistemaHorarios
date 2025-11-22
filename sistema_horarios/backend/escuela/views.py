from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Profesor, Materia, Salon, Grupo, Periodo, DisponibilidadProfesor, Horario
from .serializers import (
    ProfesorSerializer, MateriaSerializer, SalonSerializer,
    GrupoSerializer, PeriodoSerializer, DisponibilidadProfesorSerializer,
    HorarioSerializer
)
from .services import generar_horarios

class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer

class SalonViewSet(viewsets.ModelViewSet):
    queryset = Salon.objects.all()
    serializer_class = SalonSerializer

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all()
    serializer_class = GrupoSerializer

class PeriodoViewSet(viewsets.ModelViewSet):
    queryset = Periodo.objects.all()
    serializer_class = PeriodoSerializer

class DisponibilidadProfesorViewSet(viewsets.ModelViewSet):
    queryset = DisponibilidadProfesor.objects.all()
    serializer_class = DisponibilidadProfesorSerializer

class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all().order_by('dia', 'hora_inicio')
    serializer_class = HorarioSerializer

# Endpoint simple para generar
@api_view(['POST'])
def generar_horarios_view(request, periodo_id):
    generar_horarios(periodo_id)
    return Response({"detail": "Horarios generados (intentos)."})
