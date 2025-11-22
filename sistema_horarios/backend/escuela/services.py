from .models import (
    Profesor, Materia, Salon, Grupo,
    Horario, DisponibilidadProfesor, Periodo
)

def generar_horarios(periodo_id):

    periodo = Periodo.objects.get(id=periodo_id)

    grupos = Grupo.objects.all()
    profesores = Profesor.objects.all()
    salones = list(Salon.objects.all())

    for grupo in grupos:
        for profesor in profesores:

            # materias que sabe dar
            materias = profesor.materias.all()

            # horarios disponibles del profe
            disponibilidades = DisponibilidadProfesor.objects.filter(profesor=profesor)

            for materia in materias:
                for disp in disponibilidades:

                    for salon in salones:

                        try:

                            horario = Horario.objects.create(
                                periodo=periodo,
                                grupo=grupo,
                                materia=materia,
                                profesor=profesor,
                                salon=salon,
                                dia=disp.dia,
                                hora_inicio=disp.hora_inicio,
                                hora_fin=disp.hora_fin
                            )

                            print("✅ Horario creado:", horario)

                            # una vez creado pasamos al siguiente
                            break

                        except Exception as e:
                            # Si hay conflicto, sigue probando
                            # print("❌ No se pudo crear:", e)
                            pass
