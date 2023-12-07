from datetime import datetime, timedelta
from rest_framework import serializers
from .models import (
    Carga,
    Cuotas,
    HistorialEstado,
    EstadoCarga,
    CargaVehiculo,
    EstadoVehiculo,
)
from django.db import transaction
from customConfig.models import Config
from googlemaps import Client as GoogleMaps
import calendar

gm_key = "AIzaSyBBtg5zkjzwPqi5asBdnVF7zwnfwpNw6Cs"

# instancia  de Google Maps
gmaps = GoogleMaps(key=gm_key)


def distancia_kms(partida, llegada):
    # Hacer request a la API de Google Maps
    try:
        print("entramos a la función")
        resp = gmaps.distance_matrix(
            origins=partida,
            destinations=llegada,
            mode="driving",
            units="metric",
        )

        # Extraer distancia de la respuesta
        distancia = float(resp["rows"][0]["elements"][0]["distance"]["value"]) / 1000

        return distancia
    except:
        raise serializers.ValidationError("No se puede calcular la distancia")


class CargaVehiculoSerializer(serializers.ModelSerializer):
    """
    Serializer for the CargaVehiculo model.
    """

    vehiculo = serializers.CharField(source="vehiculo.__str__", read_only=True)
    nombre_conductor = serializers.CharField(
        source="conductor.first_name", read_only=True
    )
    estado = serializers.CharField(source="estado.nombre", read_only=True)

    class Meta:
        model = CargaVehiculo
        fields = [
            "id",
            "vehiculo",
            "nombre_conductor",
            "estado",
            "lat",
            "lon",
            "conductor",
        ]


class AsignarVehiculoSerializer(serializers.ModelSerializer):
    """
    Serializer for the CargaVehiculo model.
    """

    vehiculo_nombre = serializers.CharField(source="vehiculo.__str__", read_only=True)
    conductor_nombre = serializers.CharField(
        source="conductor.user.first_name", read_only=True
    )
    estado_nombre = serializers.CharField(source="estado.nombre", read_only=True)

    class Meta:
        model = CargaVehiculo
        fields = [
            "carga",
            "vehiculo_nombre",
            "conductor_nombre",
            "estado_nombre",
            "vehiculo",
            "conductor",
            "estado",
            "lon",
            "lat",
        ]
        read_only_fields = ["lon", "lat", "estado"]

    @transaction.atomic
    def create(self, validated_data):
        conductor = validated_data.get("conductor")
        if not conductor.groups.filter(name="conductores").exists():
            raise serializers.ValidationError("el conductor no existe")

        carga = validated_data.get("carga")
        estado, _ = EstadoCarga.objects.get_or_create(nombre="VEHICULO ASIGNADO")
        estado_vehiculo, _ = EstadoVehiculo.objects.get_or_create(
            nombre="VEHICULO ASIGNADO"
        )
        _ = HistorialEstado.objects.create(
            carga=carga,
            estado=estado,
            observacion="Vehiculo asignado por la empresa",
        )
        carga.estado = estado
        carga.save()

        validated_data["estado"] = estado_vehiculo
        return super().create(validated_data)


# class DireccionPartidaSerializer(serializers.ModelSerializer):
#     """
#     Serializer for the DireccionPartida model.
#     """

#     class Meta:
#         model = DireccionPartida
#         fields = ["direccion", "lat", "lon"]


# class DireccionLlegadaSerializer(serializers.ModelSerializer):
#     """
#     Serializer for the DireccionLlegada model.
#     """

#     class Meta:
#         model = DireccionLlegada
#         fields = ["direccion", "lat", "lon"]


class CuotasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuotas
        fields = ["numero_cuota", "fecha_pago", "monto_cuota", "fecha_hora_registro"]


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
    vehiculos = CargaVehiculoSerializer(
        many=True, source="carga_vehiculo", read_only=True
    )
    numero_cuotas = serializers.IntegerField(required=False, default=0, write_only=True)
    cuotas = CuotasSerializer(read_only=True, many=True)
    dia_pago = serializers.IntegerField(required=False, write_only=True)
    num_cuotas = serializers.IntegerField(source="cuotas.count", read_only=True)

    class Meta:
        model = Carga
        fields = [
            "id",
            "nombre_cliente",
            "descripcion",
            "clase_nombre",
            "monto",
            "peso",
            "tipo_nombre",
            "categoria_nombre",
            "estado_nombre",
            "fecha_hora_partida",
            "fecha_hora_llegada",
            "partida",
            "llegada",
            "vehiculos",
            "cliente",
            "clase",
            "tipo",
            "categoria",
            "estado",
            "forma_pago",
            "numero_cuotas",
            "num_cuotas",
            "dia_pago",
            "cuotas",
        ]
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

        direccion_partida = validated_data.pop("partida")
        direccion_llegada = validated_data.pop("llegada")

        distancia = distancia_kms(direccion_partida, direccion_llegada)

        monto = round(peso / 1000 * float(tarifa.valor) * distancia, 2)

        forma_pago = validated_data.pop("forma_pago")

        instance = Carga.objects.create(
            cliente=cliente,
            descripcion=descripcion,
            clase=clase,
            tipo=tipo,
            categoria=categoria,
            peso=peso,
            fecha_hora_partida=fecha_hora_partida,
            partida=direccion_partida,
            llegada=direccion_llegada,
            monto=monto,
            estado=estado,
            forma_pago=forma_pago,
        )

        _ = HistorialEstado.objects.create(carga=instance, estado=estado)

        if forma_pago == 2:
            numero_cuotas = validated_data.pop("numero_cuotas")

            monto_cuota = monto / numero_cuotas

            dia_pago = validated_data.pop("dia_pago")

            if numero_cuotas > 6:
                monto_cuota = monto_cuota * 1.1

            for i in range(numero_cuotas):
                today = datetime.today()
                month = today.month + i + 1
                year = today.year
                if month > 12:
                    month = 1 + i
                    year = year + 1

                fecha_pago = datetime(year=year, month=month, day=dia_pago)

                print("#######3")
                print(fecha_pago)

                Cuotas.objects.create(
                    carga=instance,
                    numero_cuota=i + 1,
                    fecha_pago=fecha_pago,
                    monto_cuota=monto_cuota,
                    fecha_hora_registro=datetime.now(),
                )

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
