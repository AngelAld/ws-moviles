from rest_framework import serializers
from .models import Carga, HistorialEstado, EstadoCarga
from django.db import transaction
from customConfig.models import Config


def calcularDistancia(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia entre dos puntos en coordenadas geográficas utilizando la api de google maps.
    """
    distancia = 1000

    return distancia


class AnularCargaSerializer(serializers.ModelSerializer):
    """
    Serializer for anular the Carga model.
    """

    nombre_cliente = serializers.CharField(source="cliente.first_name", read_only=True)
    anular = serializers.BooleanField(write_only=True)
    estado = serializers.CharField(source="estado.nombre", read_only=True)

    class Meta:
        model = Carga
        fields = ["id", "nombre_cliente", "descripcion", "monto", "estado", "anular"]
        read_only_fields = ["descripcion", "estado", "monto"]

    @transaction.atomic
    def update(self, instance, validated_data):
        if instance.estado.nombre != "PENDIENTE DE ATENCIÓN":
            raise serializers.ValidationError(
                "No se puede anular porque no está pendiente de atención"
            )

        estado, _ = EstadoCarga.objects.get_or_create(nombre="ANULADO")
        instance.estado = estado
        instance.save()

        new_hist = HistorialEstado.objects.create(
            carga=instance, estado=estado, observacion="Anulado por el cliente"
        )
        return instance


class CargaSerializer(serializers.ModelSerializer):
    """
    Serializer for the Carga model.
    """

    nombre_cliente = serializers.CharField(source="cliente.first_name", read_only=True)
    clase_nombre = serializers.CharField(source="clase.nombre", read_only=True)
    tipo_nombre = serializers.CharField(source="tipo.nombre", read_only=True)
    categoria_nombre = serializers.CharField(source="categoria.nombre", read_only=True)
    estado_nombre = serializers.CharField(source="estado.nombre", read_only=True)

    class Meta:
        model = Carga
        fields = "__all__"
        read_only_fields = ["estado", "fecha_hora_llegada", "monto"]

    @transaction.atomic
    def create(self, validated_data):
        cliente = validated_data.pop("cliente")

        if not cliente.groups.filter(name="clientes").exists():
            raise serializers.ValidationError("el cliente no existe")

        estado, _ = EstadoCarga.objects.get_or_create(nombre="PENDIENTE DE ATENCIÓN")
        descripcion = validated_data.pop("descripcion")

        clase = validated_data.pop("clase")
        tipo = validated_data.pop("tipo")
        categoria = validated_data.pop("categoria")
        peso = validated_data.pop("peso")
        fecha_hora_partida = validated_data.pop("fecha_hora_partida")

        tarifa, _ = Config.objects.get_or_create(
            name="tarifa", defaults={"valor": float(20)}
        )

        distancia = calcularDistancia(1, 1, 1, 1)
        monto = peso / 1000 * float(tarifa.valor) * distancia

        instance = Carga.objects.create(
            cliente=cliente,
            descripcion=descripcion,
            clase=clase,
            tipo=tipo,
            categoria=categoria,
            peso=peso,
            fecha_hora_partida=fecha_hora_partida,
            monto=monto,
            estado=estado,
        )
        _ = HistorialEstado.objects.create(carga=instance, estado=estado)
        return instance


class HistorialEstadoSerializer(serializers.ModelSerializer):
    """
    Serializer for the HistorialEstado model.
    """

    estado = serializers.CharField(source="estado.nombre")

    class Meta:
        model = HistorialEstado
        fields = ["id", "estado", "fecha_hora", "observacion"]


class CargaEstadoSerializer(serializers.ModelSerializer):
    """
    Serializer for updating estatus of  Carga model.
    """

    nombre_cliente = serializers.CharField(source="cliente.first_name", read_only=True)
    observacion = serializers.CharField(allow_blank=True, required=False)
    historial = HistorialEstadoSerializer(
        source="historial_carga", many=True, read_only=True
    )
    estado_nombre = serializers.CharField(source="estado.nombre", read_only=True)
    clase = serializers.CharField(source="clase.nombre", read_only=True)
    tipo = serializers.CharField(source="tipo.nombre", read_only=True)
    categoria = serializers.CharField(source="categoria.nombre", read_only=True)

    class Meta:
        model = Carga
        fields = [
            "id",
            "nombre_cliente",
            "descripcion",
            "estado_nombre",
            "clase",
            "tipo",
            "categoria",
            "peso",
            "fecha_hora_partida",
            "fecha_hora_llegada",
            "estado",
            "observacion",
            "historial",
        ]
        read_only_fields = (
            "id",
            "cliente",
            "descripcion",
            "clase",
            "tipo",
            "categoria",
            "peso",
            "fecha_hora_partida",
            "fecha_hora_llegada",
            "monto",
        )

    @transaction.atomic
    def update(self, instance, validated_data):
        print(validated_data)
        new_estado = validated_data.get("estado")
        new_observacion = validated_data.get("observacion")
        if new_estado != instance.estado:
            new_hist = HistorialEstado.objects.create(
                carga=instance, estado=new_estado, observacion=new_observacion
            )
        return super().update(instance, validated_data)


class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoCarga
        fields = "__all__"
