# Generated by Django 3.1.3 on 2020-11-13 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0005_auto_20201112_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alimentuser',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Nombre Alimento'),
        ),
    ]
