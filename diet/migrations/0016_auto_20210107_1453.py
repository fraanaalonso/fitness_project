# Generated by Django 3.1.3 on 2021-01-07 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diet', '0015_auto_20201226_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aliment',
            name='gr_hc',
            field=models.CharField(max_length=4, verbose_name='Gramos de Hidratos de Carbono'),
        ),
        migrations.AlterField(
            model_name='aliment',
            name='gr_lip',
            field=models.CharField(max_length=4, verbose_name='Gramos de Grasas'),
        ),
        migrations.AlterField(
            model_name='aliment',
            name='gr_pr',
            field=models.CharField(max_length=4, verbose_name='Gramos de Proteínas'),
        ),
    ]
