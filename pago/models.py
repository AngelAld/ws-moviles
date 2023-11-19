from django.db import models
from carga.models import Carga

# Create your models here.


class EstadoPago(models.Model):
    nombre = models.CharField(max_length=100)


class Pago(models.Model):
    carga = models.ForeignKey(Carga, on_delete=models.CASCADE)
    nombre_entidad = models.CharField(max_length=100)
    numero_operacion = models.CharField(max_length=100)
    fecha_hora_operacion = models.DateTimeField()
    voucher = models.CharField(max_length=200)
    estado = models.ForeignKey(
        EstadoPago, on_delete=models.PROTECT, related_name="estado"
    )
