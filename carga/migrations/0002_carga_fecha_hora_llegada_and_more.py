# Generated by Django 4.2.7 on 2023-11-20 15:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('carga', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carga',
            name='fecha_hora_llegada',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='carga',
            name='fecha_hora_partida',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='historialestado',
            name='fecha_hora',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
