from rest_framework import serializers
from .models import EstadoPago, Pago
from carga.models import Carga
from cliente.models import Cliente
from django.contrib.auth.models import User
from carga.serializers import CargaSerializer


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
    estado_nombre = serializers.CharField(source="estado")

    class Meta:
        model = Pago
        fields = "__all__"
