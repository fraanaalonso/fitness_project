# Generated by Django 3.1.1 on 2020-11-04 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0007_auto_20201104_1705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='practice',
            name='number_training',
        ),
        migrations.AddField(
            model_name='practice',
            name='training_id',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='training.training'),
            preserve_default=False,
        ),
    ]
