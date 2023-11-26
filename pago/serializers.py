from rest_framework import serializers
from .models import EstadoPago, Pago
from carga.models import Carga
from cliente.models import Cliente
from django.contrib.auth.models import User
from carga.serializers import CargaSerializer
from django.db.transaction import atomic


class EstadoPagoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo EstadoPago
    """

    class Meta:
        model = EstadoPago
        fields = "__all__"


class PagoSerializer(serializers.ModelSerializer):
    carga_desc = serializers.CharField(read_only=True, source="carga.descripcion")
    """
    Serializer para el modelo Pago
    """
    estado_nombre = serializers.CharField(source="estado", read_only=True)

    class Meta:
        model = Pago
        fields = "__all__"
        read_only_fields = ["estado"]

    @atomic
    def create(self, validated_data):
        estado, _ = EstadoPago.objects.get_or_create(nombre="PENDIENTE DE ATENCIÓN")
        validated_data["estado"] = estado
        return super().create(validated_data)


class ConfirmarPagoSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Pago
    """

    carga_desc = serializers.CharField(read_only=True, source="carga.descripcion")

    estado_nombre = serializers.CharField(source="estado", read_only=True)

    class Meta:
        model = Pago
        fields = "__all__"
        read_only_fields = [
            "carga",
            "nombre_entidad",
            "numero_operacion",
            "fecha_hora_operacion",
            "voucher",
        ]

    @atomic
    def update(self, instance, validated_data):
        instance.estado = validated_data.get("estado", instance.estado)
        instance.save()
        return instance
