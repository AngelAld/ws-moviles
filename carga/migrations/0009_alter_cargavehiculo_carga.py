# Generated by Django 4.2.7 on 2023-11-27 00:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carga', '0008_alter_cargavehiculo_carga_delete_historialvehiculo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargavehiculo',
            name='carga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carga_vehiculo', to='carga.carga'),
        ),
    ]
