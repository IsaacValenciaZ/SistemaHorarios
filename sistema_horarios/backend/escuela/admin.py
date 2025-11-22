from django.contrib import admin
from .models import (
    Profesor, Alumno, Materia, Salon, Grupo, Periodo,
    DisponibilidadProfesor, Horario
)

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'especialidad')
    filter_horizontal = ('materias',)  # para mover materias fácil

admin.site.register(Alumno)
admin.site.register(Materia)
admin.site.register(Salon)
admin.site.register(Grupo)
admin.site.register(Periodo)
admin.site.register(DisponibilidadProfesor)
admin.site.register(Horario)
