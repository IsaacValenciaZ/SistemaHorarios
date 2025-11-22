from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q

# ---------- CATÁLOGOS ----------

class Profesor(models.Model):
    nombre = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    especialidad = models.CharField(max_length=150, blank=True)

    materias = models.ManyToManyField('Materia', blank=True, related_name='profesores')

    def __str__(self):
        return self.nombre


class Alumno(models.Model):
    nombre = models.CharField(max_length=150)
    matricula = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.matricula} - {self.nombre}"


class Materia(models.Model):
    nombre = models.CharField(max_length=120)
    codigo = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Salon(models.Model):
    nombre = models.CharField(max_length=50)
    capacidad = models.PositiveIntegerField(default=30)

    def __str__(self):
        return self.nombre


class Grupo(models.Model):
    nombre = models.CharField(max_length=50)
    alumnos = models.ManyToManyField(Alumno, blank=True)

    def __str__(self):
        return self.nombre


class Periodo(models.Model):
    nombre = models.CharField(max_length=20)  # e.g. "2026/1"
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activo = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


# ---------- DISPONIBILIDAD del profesor ----------
# (Esto permite que declares cuando el profesor está disponible)

class DisponibilidadProfesor(models.Model):
    DIAS = [
        ("LUN", "Lunes"),
        ("MAR", "Martes"),
        ("MIE", "Miércoles"),
        ("JUE", "Jueves"),
        ("VIE", "Viernes"),
        ("SAB", "Sábado"),
    ]

    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='disponibilidades')
    dia = models.CharField(max_length=3, choices=DIAS)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        verbose_name = "Disponibilidad Profesor"
        verbose_name_plural = "Disponibilidades Profesores"

    def __str__(self):
        return f"{self.profesor} - {self.get_dia_display()} {self.hora_inicio.strftime('%H:%M')}-{self.hora_fin.strftime('%H:%M')}"


# ---------- HORARIO (validaciones críticas) ----------

class Horario(models.Model):
    DIAS = DisponibilidadProfesor.DIAS

    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='horarios')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='horarios')
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='horarios')

    dia = models.CharField(max_length=3, choices=DIAS)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"

    def __str__(self):
        return f"{self.periodo} | {self.grupo} | {self.materia} | {self.get_dia_display()} {self.hora_inicio}-{self.hora_fin}"

    def clean(self):
        # 1) rango de horas coherente
        if self.hora_fin <= self.hora_inicio:
            raise ValidationError("La hora_fin debe ser posterior a hora_inicio.")

        # 2) profesor enseña la materia?
        if not self.profesor.materias.filter(pk=self.materia.pk).exists():
            raise ValidationError("El profesor no está registrado para impartir esta materia.")

        # 3) el profesor está disponible en ese día y franja horaria?
        dispon = DisponibilidadProfesor.objects.filter(
            profesor=self.profesor,
            dia=self.dia,
            hora_inicio__lte=self.hora_inicio,
            hora_fin__gte=self.hora_fin
        )
        if not dispon.exists():
            raise ValidationError("El profesor NO tiene disponibilidad registrada para esa franja (dia/hora).")

        # 4) NO deberá existir empalme para:
        #    - mismo profesor
        #    - mismo salón
        #    - mismo grupo
        conflictos = Horario.objects.filter(
            periodo=self.periodo,
            dia=self.dia,
            hora_inicio__lt=self.hora_fin,
            hora_fin__gt=self.hora_inicio
        ).filter(
            Q(profesor=self.profesor) |
            Q(salon=self.salon) |
            Q(grupo=self.grupo)
        ).exclude(id=self.id)

        if conflictos.exists():
            # mostrar detalles en el mensaje puede ayudar en admin
            primera = conflictos.first()
            raise ValidationError(f"Conflicto con otro horario: {primera}.")

    def save(self, *args, **kwargs):
        # Ejecuta validaciones antes de guardar (útil para Admin/API)
        self.clean()
        super().save(*args, **kwargs)


