from rest_framework import serializers
from .models import Carga, HistorialEstado
from django.db import transaction


class CargaSerializer(serializers.ModelSerializer):
    """
    Serializer for the Carga model.
    """

    nombre_cliente = serializers.CharField(source="cliente.first_name", read_only=True)
    observacion = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Carga
        fields = "__all__"


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
