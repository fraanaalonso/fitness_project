# Generated by Django 3.1.3 on 2020-12-09 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0010_auto_20201208_2347'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='practice',
            options={'verbose_name': 'Ejercicios Entrenamiento Usuario'},
        ),
        migrations.AddField(
            model_name='exercise',
            name='categoria',
            field=models.CharField(default='Calentamiento', max_length=20, verbose_name='Categoría Ejercicio'),
            preserve_default=False,
        ),
    ]
