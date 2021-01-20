# Generated by Django 3.1.1 on 2020-11-04 10:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('training', '0004_auto_20201103_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practice',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.exercise', verbose_name='Ejercicio'),
        ),
        migrations.AlterField(
            model_name='practice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Cliente'),
        ),
    ]
