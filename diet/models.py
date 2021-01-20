from django.db import models
from ckeditor.fields import RichTextField
from user.models import User


class DietType(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=50, help_text="Required")
    description = RichTextField(verbose_name="Descripcion", help_text="Required")
    hc_percentage = models.CharField(verbose_name="% Hidratos de Carbono", help_text="Required", max_length=3)
    pr_percentage = models.CharField(verbose_name="% Proteinas", help_text="Required", max_length=3)
    gr_percentage = models.CharField(verbose_name="% Lípidos", help_text="Required", max_length=3)

    class Meta:
        verbose_name = "Tipo Dieta"

    def __str__(self):
        return self.name


class Aliment(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=100, help_text="Required")
    kcal_hundred_gr = models.FloatField(max_length=5, verbose_name="Kcal 100 gramos")
    gr_hc = models.FloatField(max_length=5, verbose_name="Gramos de Hidratos de Carbono")
    gr_pr = models.FloatField(max_length=5, verbose_name="Gramos de Proteínas")
    gr_lip = models.FloatField(max_length=5, verbose_name="Gramos de Grasas")

    class Meta:
        verbose_name = "Alimento"
        verbose_name_plural = "Alimentos"

    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=20, help_text="Required")
    description = RichTextField(verbose_name="Descripcion", help_text="Required")
    hc_gramos = models.FloatField(verbose_name="Gramos Hidratos de Carbono", max_length=20)
    pr_gramos = models.FloatField(verbose_name="Gramos Proteínas", max_length=20)
    gr_gramos = models.FloatField(verbose_name="Gramos Grasas", max_length=20)
    class Meta:
        verbose_name = "Comida"

    def __str__(self):
        return self.name


class Diet(models.Model):
    name = models.CharField(verbose_name="Nombre", max_length=50, help_text="required", null=True, blank=True)
    description = RichTextField(verbose_name="Descripcion Dieta", null=True, blank=True)
    type_diet = models.ForeignKey(DietType,  verbose_name="Tipo Dieta", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.CASCADE, related_name="Usuario Cliente+")
    aliments = models.ManyToManyField(Aliment, through="AlimentUser")
    calorias = models.CharField(max_length=30, help_text="required", verbose_name="Calorías de la Dieta")
    meals = models.ManyToManyField(Meal, through="MealUser")
    calorias_hc = models.CharField(max_length=30, help_text="required", verbose_name="Calorías HC")
    calorias_pr = models.CharField(max_length=30, help_text="required", verbose_name="Calorías PR")
    calorias_gr = models.CharField(max_length=30, help_text="required", verbose_name="Calorías GR")
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(verbose_name="Fecha Fin")
    visible = models.BooleanField(verbose_name="¿Visible?")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Usuario entrenador+")
    class Meta:
        verbose_name = "Dieta"

    def __str__(self):
        return self.name


class MealUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    day = models.DateField("Día", max_length=20)
    comments = RichTextField(verbose_name="Comentarios Adicionales")
    meal_number = models.IntegerField(verbose_name="Número de Comida")
    class Meta:
        verbose_name="Comidas Usuario"
        
    def __str__(self):
        return str(self.meal)

class AlimentUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    diet = models.ForeignKey(Diet, on_delete=models.CASCADE)
    aliment = models.ForeignKey(Aliment, on_delete=models.CASCADE)
    day = models.DateField("Día", max_length=20)
    comments = RichTextField(verbose_name="Comentarios Adicionales")
    gramos = models.FloatField(verbose_name="Gramos Alimento", max_length=20)
    meal_number = models.IntegerField(verbose_name="Número de Comida")
    class Meta:
        verbose_name="Alimentos Usuario"
        
    def __str__(self):
        return self.aliment