from django.db import models
from user.models import User, Tariff
# Create your models here.



class Payment(models.Model):
    description = models.CharField(max_length=150, help_text="required", verbose_name="Descripción")
    id_client = models.ForeignKey(User, help_text="Required", verbose_name="Cliente", on_delete=models.CASCADE)
    quantity = models.FloatField(help_text="Required", verbose_name="Cantidad a pagar")
    initial_date = models.DateField(help_text="Required", verbose_name="Fecha de Inicio")
    dead_line = models.DateField(help_text="Required", verbose_name="Fecha Límite")


    class Meta:
        verbose_name="Pago"
        verbose_name_plural="Pagos"

    
    def __str__(self):
        return self.id_client