# Generated by Django 3.1.3 on 2020-11-13 19:53

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_user_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='meals',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Numero de Comidas'),
        ),
    ]
