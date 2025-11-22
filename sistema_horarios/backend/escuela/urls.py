from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProfesorViewSet, MateriaViewSet, SalonViewSet, GrupoViewSet,
    PeriodoViewSet, DisponibilidadProfesorViewSet, HorarioViewSet,
    generar_horarios_view
)

router = DefaultRouter()
router.register('profesores', ProfesorViewSet)
router.register('materias', MateriaViewSet)
router.register('salones', SalonViewSet)
router.register('grupos', GrupoViewSet)
router.register('periodos', PeriodoViewSet)
router.register('disponibilidades', DisponibilidadProfesorViewSet)
router.register('horarios', HorarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('generar/<int:periodo_id>/', generar_horarios_view, name='generar-horarios'),
]
