from django.db import models
from carga.models import Carga

# Create your models here.


class EstadoPago(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nombre


class Pago(models.Model):
    carga = models.ForeignKey(Carga, on_delete=models.CASCADE)
    nombre_entidad = models.CharField(max_length=100)
    numero_operacion = models.CharField(max_length=100)
    fecha_hora_operacion = models.DateTimeField()
    voucher = models.ImageField(upload_to="pago/vouchers/")
    estado = models.ForeignKey(
        EstadoPago, on_delete=models.PROTECT, related_name="estado"
    )
