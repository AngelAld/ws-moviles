from django.db import models
from django.contrib.auth.models import User
from conductor.models import Conductor, Vehiculo
from django.utils.timezone import now

# Create your models here.


class ClaseCarga(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nombre


class TipoCarga(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nombre


class CategoriaCarga(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nombre


class EstadoCarga(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nombre


class EstadoVehiculo(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nombre


class Carga(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.PROTECT, related_name="cliente")
    descripcion = models.CharField(max_length=100)
    clase = models.ForeignKey(
        ClaseCarga, on_delete=models.PROTECT, related_name="clase"
    )
    tipo = models.ForeignKey(TipoCarga, on_delete=models.PROTECT, related_name="tipo")
    categoria = models.ForeignKey(
        CategoriaCarga, on_delete=models.PROTECT, related_name="categoria"
    )
    peso = models.FloatField()
    fecha_hora_partida = models.DateTimeField()
    fecha_hora_llegada = models.DateTimeField(null=True, blank=True)
    monto = models.FloatField()
    estado = models.ForeignKey(
        EstadoCarga, on_delete=models.PROTECT, related_name="estado_actual"
    )
    partida = models.CharField(max_length=400)
    llegada = models.CharField(max_length=400)
    forma_pago = models.IntegerField(default=1)


class Cuotas(models.Model):
    carga = models.ForeignKey(Carga, on_delete=models.CASCADE, related_name="cuotas")
    numero_cuota = models.IntegerField()
    fecha_pago = models.DateTimeField()
    monto_cuota = models.FloatField()
    fecha_hora_registro = models.DateTimeField()


# class DireccionPartida(models.Model):
#     carga = models.OneToOneField(
#         Carga, on_delete=models.CASCADE, related_name="direccion_partida"
#     )
#     direccion = models.CharField(max_length=100)
#     lon = models.CharField(max_length=100)
#     lat = models.CharField(max_length=100)


# class DireccionLlegada(models.Model):
#     carga = models.OneToOneField(
#         Carga, on_delete=models.CASCADE, related_name="direccion_llegada"
#     )
#     direccion = models.CharField(max_length=100)
#     lon = models.CharField(max_length=100)
#     lat = models.CharField(max_length=100)


class HistorialEstado(models.Model):
    carga = models.ForeignKey(
        Carga, on_delete=models.CASCADE, related_name="historial_carga"
    )
    estado = models.ForeignKey(
        EstadoCarga, on_delete=models.PROTECT, related_name="estado"
    )
    fecha_hora = models.DateTimeField(default=now)
    observacion = models.CharField(max_length=300, blank=True, null=True)


class CargaVehiculo(models.Model):
    carga = models.ForeignKey(
        Carga, on_delete=models.CASCADE, related_name="carga_vehiculo"
    )
    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.PROTECT, related_name="vehiculo"
    )
    conductor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="conductor"
    )
    lon = models.CharField(max_length=100, blank=True, null=True)
    lat = models.CharField(max_length=100, blank=True, null=True)
    estado = models.ForeignKey(
        EstadoVehiculo, on_delete=models.PROTECT, related_name="estado_actual"
    )

    def __str__(self) -> str:
        return (
            self.carga.descripcion
            + " "
            + self.vehiculo.placa
            + " "
            + self.conductor.first_name
        )


# class HistorialVehiculo(models.Model):
#     carga_vehiculo = models.ForeignKey(
#         CargaVehiculo, on_delete=models.PROTECT, related_name="carga_vehiculo"
#     )
#     estado = models.ForeignKey(
#         EstadoVehiculo, on_delete=models.PROTECT, related_name="estado"
#     )
#     fecha_hora = models.DateTimeField()
#     observacion = models.CharField(max_length=300)
