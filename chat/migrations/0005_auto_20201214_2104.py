# Generated by Django 3.1.3 on 2020-12-14 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20201214_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha mensaje'),
        ),
    ]
