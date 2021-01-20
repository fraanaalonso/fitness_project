from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, Group
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField
from random import randrange
from django.core.files.storage import FileSystemStorage
from datetime import  date, datetime
import datetime

CHARSET = 'abcdefghijklrmnopqrstuvwxyz'
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, staff=False, is_superuser=False, active=False, grupo='2'):
        if not email:
            raise ValueError("Los usuarios deben de tener una dirección de e-mail")
        
        if not password:
            raise ValueError("Los usuarios deben tener pass")
        
        user = self.model(
            email = self.normalize_email(email)

        )
        user.set_password(password)
        user.save(using=self._db)
        user.staff=staff
        user.active=active
        user.is_superuser=is_superuser
        user.grupo = grupo
        return user

    def create_staffUser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            staff=True
        )

        return user


    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            staff=True,
            is_superuser=True,
            active=True
        )

        return user

    
            
class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    is_trainer = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name="Entrena", verbose_name="Entrenador")
    first_name = models.CharField(max_length=30, blank=True, help_text="required")
    last_name = models.CharField(max_length=30, blank=True, help_text="required")
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Grupo")
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    objects = UserManager()

    def guardarUsername(self, *args, **kwargs):      
        loop_num = 0
        unique = False
        while not unique:
            if loop_num < 32:
                new_username = ''
                for i in range(16): 
                    new_username += CHARSET[randrange(0, len(CHARSET))]
                if not User.objects.filter(username=new_username):
                    self.username = new_username
                    unique = True
                loop_num += 1
            else:
                raise ValueError("No se ha podido generar el código")
        super(User, self).save(*args, **kwargs)

    
    def calc_edad(self, nac):
        hoy = date.today()
        edad = hoy.year - nac
        
        return edad

    def get_full_name(self):
        return self.email
    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.is_superuser
    
    def __str__(self):
        return self.email


class Tariff(models.Model):
    typeTariff = models.CharField(max_length=50, verbose_name='Tipo')
    content = RichTextField(verbose_name="Contenido")
    price = models.CharField(verbose_name="Precio", max_length=10)
    duracion = models.CharField(verbose_name="Duración del Plan", max_length=3, null=True)

    class Meta:
        verbose_name = "Tarifa"
        verbose_name_plural = "Tarifas"


    def __str__(self):
        return self.content

fs = FileSystemStorage(location='/media/profile-photos')
class Record(models.Model):

    OPTIONS_SOMATOTIPE = (
        ('EC', 'Ectomorfo'),
        ('ME', 'Mesomorfo'),
        ('EN', 'Endomorfo')
    )

    OPTIONS_GENDER = (
        ('Hombre', 'Masculino'),
        ('Mujer', 'Femenino')
    )
   
    dni = models.CharField(max_length=9, help_text="required", verbose_name="DNI", null=True, blank=True)
    phone = models.CharField(max_length=9, help_text="required", verbose_name="Teléfono", null=True, blank=True)
    photo = models.ImageField(upload_to="profile-photos", verbose_name="Fotos Subidas")
    date = models.DateField(verbose_name="Fecha de Nacimiento", null=True, blank=True)
    country = models.CharField(verbose_name="País", help_text="Required", max_length=50, null=True, blank=True)
    weight = models.CharField(verbose_name="Peso", help_text="Required", max_length=3, null=True, blank=True)
    height = models.CharField(verbose_name="Altura", help_text="Required", max_length=3, null=True, blank=True)
    somatotipe = models.CharField(help_text="Required", verbose_name="Somatotipo", choices=OPTIONS_SOMATOTIPE, max_length=10, null=True, blank=True)
    userID = models.ForeignKey(User, verbose_name="Usuario", on_delete=models.CASCADE)
    gender = models.CharField(help_text="Required", verbose_name="Género", choices=OPTIONS_GENDER, max_length=10, null=True, blank=True)
    timing = RichTextField(verbose_name="Horarios", null=True, blank=True)
    meals = RichTextField(verbose_name="Numero de Comidas", null=True, blank=True)
    patologies = RichTextField(verbose_name="Patologias", null=True, blank=True)
    sports = RichTextField(verbose_name="Deportes", null=True, blank=True)
    comments = RichTextField(verbose_name="Comentarios", null=True, blank=True)
    plan = models.ForeignKey(Tariff, verbose_name="Plan seleccionado", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Ficha Técnica Usuario'
        verbose_name_plural="Ficha Técnicas Usuarios"

    def __str__(self):
        return str(self.userID)


class Image(models.Model):
    description = RichTextField(verbose_name="Descripcion")
    image = models.ImageField(upload_to="profile-photos", verbose_name="Fotos Subidas")
    user = models.ManyToManyField(User)
    peso = models.IntegerField(verbose_name="Peso Usuario")
    fecha_subida = models.DateField(auto_now=True, verbose_name="Fecha Subida")
    def __str__(self):
        return str(self.id)


