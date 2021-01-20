# Generated by Django 3.1.3 on 2020-12-13 20:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True, verbose_name='Fecha mensaje')),
                ('content', models.CharField(max_length=200, verbose_name='Contenido')),
                ('emisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Usuario emisor+', to=settings.AUTH_USER_MODEL, verbose_name='Emisor')),
                ('receptor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Usuario receptor+', to=settings.AUTH_USER_MODEL, verbose_name='Receptor')),
            ],
            options={
                'verbose_name': 'Chat',
            },
        ),
    ]
