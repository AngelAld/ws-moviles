# Generated by Django 4.2.7 on 2023-11-19 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0003_alter_cliente_doc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='doc',
            field=models.CharField(max_length=20),
        ),
    ]
