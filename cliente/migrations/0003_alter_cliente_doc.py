# Generated by Django 4.2.7 on 2023-11-19 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0002_remove_cliente_name_rs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='doc',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
