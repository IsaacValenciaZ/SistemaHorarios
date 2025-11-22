from rest_framework import serializers
from .models import (
    Profesor, Alumno, Materia, Salon, Grupo, Periodo,
    DisponibilidadProfesor, Horario
)

class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = '__all__'

class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = '__all__'

class SalonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salon
        fields = '__all__'

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = '__all__'

class PeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodo
        fields = '__all__'

class DisponibilidadProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisponibilidadProfesor
        fields = '__all__'

class HorarioSerializer(serializers.ModelSerializer):
    periodo = PeriodoSerializer(read_only=True)
    grupo = GrupoSerializer(read_only=True)
    profesor = ProfesorSerializer(read_only=True)
    materia = MateriaSerializer(read_only=True)
    salon = SalonSerializer(read_only=True)

    periodo_id = serializers.PrimaryKeyRelatedField(
        source='periodo', queryset=Periodo.objects.all(), write_only=True
    )
    grupo_id = serializers.PrimaryKeyRelatedField(
        source='grupo', queryset=Grupo.objects.all(), write_only=True
    )
    profesor_id = serializers.PrimaryKeyRelatedField(
        source='profesor', queryset=Profesor.objects.all(), write_only=True
    )
    materia_id = serializers.PrimaryKeyRelatedField(
        source='materia', queryset=Materia.objects.all(), write_only=True
    )
    salon_id = serializers.PrimaryKeyRelatedField(
        source='salon', queryset=Salon.objects.all(), write_only=True
    )

    class Meta:
        model = Horario
        fields = [
            'id', 'periodo', 'periodo_id', 'grupo', 'grupo_id', 'materia', 'materia_id',
            'profesor', 'profesor_id', 'salon', 'salon_id',
            'dia', 'hora_inicio', 'hora_fin'
        ]
