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
    fecha_hora_partida = models.DateTimeField(default=now)
    fecha_hora_llegada = models.DateTimeField(null=True, blank=True)
    monto = models.FloatField()
    estado = models.ForeignKey(
        EstadoCarga, on_delete=models.PROTECT, related_name="estado_actual"
    )


class DireccionPartida(models.Model):
    carga = models.ForeignKey(
        Carga, on_delete=models.PROTECT, related_name="partida_carga"
    )
    direccion = models.CharField(max_length=100)
    lon = models.CharField(max_length=100)
    lat = models.CharField(max_length=100)


class DireccionLlegada(models.Model):
    carga = models.ForeignKey(
        Carga, on_delete=models.PROTECT, related_name="llegada_carga"
    )
    direccion = models.CharField(max_length=100)
    lon = models.CharField(max_length=100)
    lat = models.CharField(max_length=100)


class HistorialEstado(models.Model):
    carga = models.ForeignKey(
        Carga, on_delete=models.PROTECT, related_name="historial_carga"
    )
    estado = models.ForeignKey(
        EstadoCarga, on_delete=models.PROTECT, related_name="estado"
    )
    fecha_hora = models.DateTimeField(default=now)
    observacion = models.CharField(max_length=300, blank=True, null=True)


class CargaVehiculo(models.Model):
    carga = models.ForeignKey(Carga, on_delete=models.PROTECT, related_name="carga")
    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.PROTECT, related_name="vehiculo"
    )
    conductor = models.ForeignKey(
        Conductor, on_delete=models.PROTECT, related_name="conductor"
    )
    lon = models.CharField(max_length=100)
    lat = models.CharField(max_length=100)
    estado = models.ForeignKey(
        EstadoVehiculo, on_delete=models.PROTECT, related_name="estado_actual"
    )


class HistorialVehiculo(models.Model):
    carga_vehiculo = models.ForeignKey(
        CargaVehiculo, on_delete=models.PROTECT, related_name="carga_vehiculo"
    )
    estado = models.ForeignKey(
        EstadoVehiculo, on_delete=models.PROTECT, related_name="estado"
    )
    fecha_hora = models.DateTimeField()
    observacion = models.CharField(max_length=300)
