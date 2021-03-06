# Generated by Django 3.1.1 on 2020-11-02 20:34

import ckeditor.fields
from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('username', models.CharField(max_length=30, unique=True)),
                ('first_name', models.CharField(blank=True, help_text='required', max_length=30)),
                ('last_name', models.CharField(blank=True, help_text='required', max_length=30)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=True)),
                ('is_trainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Entrena', to=settings.AUTH_USER_MODEL, verbose_name='Entrenador')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tariff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeTariff', models.CharField(max_length=50, verbose_name='Tipo')),
                ('content', ckeditor.fields.RichTextField(verbose_name='Contenido')),
                ('price', models.CharField(max_length=10, verbose_name='Precio')),
                ('duracion', models.CharField(max_length=3, null=True, verbose_name='Duración del Plan')),
            ],
            options={
                'verbose_name': 'Tarifa',
                'verbose_name_plural': 'Tarifas',
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(blank=True, help_text='required', max_length=9, null=True, verbose_name='DNI')),
                ('phone', models.CharField(blank=True, help_text='required', max_length=9, null=True, verbose_name='Teléfono')),
                ('photo', models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/media/profile-photos'), upload_to='', verbose_name='Foto de Perfil')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento')),
                ('country', models.CharField(blank=True, help_text='Required', max_length=50, null=True, verbose_name='País')),
                ('weight', models.CharField(blank=True, help_text='Required', max_length=3, null=True, verbose_name='Peso')),
                ('height', models.CharField(blank=True, help_text='Required', max_length=3, null=True, verbose_name='Altura')),
                ('somatotipe', models.CharField(blank=True, choices=[('EC', 'Ectomorfo'), ('ME', 'Mesomorfo'), ('EN', 'Endomorfo')], help_text='Required', max_length=10, null=True, verbose_name='Somatotipo')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Femenino')], help_text='Required', max_length=10, null=True, verbose_name='Género')),
                ('timing', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Horarios')),
                ('meals', ckeditor.fields.RichTextField(blank=True, help_text='Required', null=True, verbose_name='Numero de Comidas')),
                ('patologies', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Patologias')),
                ('sports', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Deportes')),
                ('comments', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Comentarios')),
                ('plan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.tariff', verbose_name='Plan seleccionado')),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Ficha Técnica Usuario',
                'verbose_name_plural': 'Ficha Técnicas Usuarios',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', ckeditor.fields.RichTextField(verbose_name='Descripcion')),
                ('image', models.ImageField(upload_to='profile-photos', verbose_name='Fotos Subidas')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
