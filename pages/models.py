from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Page(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    content = RichTextField(verbose_name="Contenido")
    public = models.BooleanField(verbose_name='¿Visible?')
    order = models.IntegerField(verbose_name="Orden")
    slug = models.CharField(unique=True, max_length=100, verbose_name='URL Amigable')

    class Meta:
        verbose_name = "Pagina"
        verbose_name_plural = "Paginas"


    def __str__(self):
        return self.name
