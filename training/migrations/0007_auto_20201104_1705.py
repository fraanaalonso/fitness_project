# Generated by Django 3.1.1 on 2020-11-04 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0006_practice_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practice',
            name='day',
            field=models.CharField(max_length=20, verbose_name='Día'),
        ),
    ]
