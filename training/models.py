from django.db import models
from user.models import User, Record
from ckeditor.fields import RichTextField
# Create your models here.



class Exercise(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=20)
    description = RichTextField(verbose_name="Descripción")
    image = models.ImageField(verbose_name="Imagen del ejercicio", upload_to="exercise-photos")
    video = models.FileField(verbose_name="Video del ejercicio", upload_to="exercise-videos")
    user = models.ManyToManyField(User, through="Practice")
    categoria = models.CharField(max_length=20, verbose_name="Categoría Ejercicio")

    def __str__(self):
        return self.name + " - " + self.categoria

    class Meta:
        verbose_name="Ejercicio"
        verbose_name_plural = "Ejercicios"



class Training(models.Model):
    name = models.CharField(verbose_name="Nombre", help_text="Required", max_length=50)
    description = RichTextField(verbose_name="Descripción", help_text="Required")
    exercise = models.ManyToManyField(Exercise)
    user = models.ForeignKey(User, verbose_name="Entrenador Usuario", on_delete=models.CASCADE)
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio", help_text="Required")
    fecha_fin = models.DateField(verbose_name="Fecha Fin", help_text="Required")
    visible = models.BooleanField(verbose_name="¿Visible?", help_text="Required")
    created_by = models.ForeignKey(User, verbose_name="Entrenador", related_name="Usuario Entrnador+", on_delete=models.CASCADE)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name="Entrenamiento"
        verbose_name_plural = "Entrenamientos"

class Practice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Cliente")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, verbose_name="Ejercicio")
    series = models.CharField(max_length=10, verbose_name="Numero de series", null=True, blank=True)
    reps = models.CharField(max_length=120, verbose_name="Repeticiones del ejercicio", null=True, blank=True)
    stop = models.CharField(max_length=20, verbose_name="Tiempo de descanso", null=True, blank=True)
    comments = RichTextField(verbose_name="Comentarios")
    training_id = models.ForeignKey(Training, on_delete=models.CASCADE)
    day = models.CharField(max_length=20, verbose_name="Día")
    def __str__(self):
        return self.user

    class Meta:
        verbose_name="Ejercicios Entrenamiento Usuario"