# Generated by Django 3.1.1 on 2020-11-02 20:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='required', max_length=150, verbose_name='Descripción')),
                ('initial_date', models.DateField(help_text='Required', verbose_name='Fecha de Inicio')),
                ('dead_line', models.DateField(help_text='Required', verbose_name='Fecha Límite')),
                ('id_client', models.ForeignKey(help_text='Required', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Cliente')),
                ('quantity', models.ForeignKey(help_text='Required', on_delete=django.db.models.deletion.CASCADE, to='user.tariff', verbose_name='Cantidad a pagar')),
            ],
            options={
                'verbose_name': 'Pago',
                'verbose_name_plural': 'Pagos',
            },
        ),
    ]
