from rest_framework import serializers
from .models import Conductor, Vehiculo
from django.contrib.auth.models import User, Group
from django.db import transaction
from usuario.models import Status
from carga.models import CargaVehiculo, EstadoVehiculo


class ConductorProfileSerializer(serializers.ModelSerializer):
    docTypeName = serializers.StringRelatedField(source="doc_type")
    statusName = serializers.StringRelatedField(source="status")

    class Meta:
        model = Conductor
        fields = [
            "doc",
            "docTypeName",
            "statusName",
            "address",
            "cel",
            "doc_type",
            "status",
        ]
        read_only_fields = ("docTypeName", "statusName", "status", "user")


class ConductorAdminProfileSerializer(serializers.ModelSerializer):
    docTypeName = serializers.StringRelatedField(source="docType")
    statusName = serializers.StringRelatedField(source="status")

    class Meta:
        model = Conductor
        fields = [
            "doc",
            "docTypeName",
            "statusName",
            "address",
            "cel",
            "doc_type",
            "status",
        ]
        read_only_fields = (
            "docTypeName",
            "statusName",
            "doc",
            "address",
            "cel",
            "doc_type",
        )


class ConductorSerializer(serializers.ModelSerializer):
    conductor = ConductorProfileSerializer(source="conductor_profile", many=False)
    name_rs = serializers.CharField(source="first_name")

    class Meta:
        model = User
        fields = (
            "id",
            "name_rs",
            "email",
            "password",
            "is_active",
            "conductor",
        )
        read_only_fields = ("id", "is_active")
        extra_kwargs = {"password": {"write_only": True}}

    @transaction.atomic
    def update(self, instance, validated_data):
        conductor_profile = instance.conductor_profile
        conductor_profile_data = validated_data.pop("conductor_profile", {})

        conductor_profile.doc = conductor_profile_data.get("doc", conductor_profile.doc)
        conductor_profile.address = conductor_profile_data.get(
            "address", conductor_profile.address
        )
        conductor_profile.cel = conductor_profile_data.get("cel", conductor_profile.cel)
        conductor_profile.doc_type = conductor_profile_data.get(
            "doc_type", conductor_profile.doc_type
        )

        conductor_profile.save()

        instance.username = validated_data.get("email", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.set_password(validated_data.get("password", instance.password))
        instance.email = validated_data.get("email", instance.email)
        instance.save()

        return instance

    @transaction.atomic
    def create(self, validated_data):
        try:
            conductor_profile_data = validated_data.pop("conductor_profile", {})
            email = validated_data.get("email", None)
            first_name = validated_data.get("first_name", None)
            username = validated_data.get("email", None)
            password = validated_data.get("password", None)

            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                is_active=False,
            )

            status, _ = Status.objects.get_or_create(name="PENDIENTE DE VALIDACIÓN")

            conductor = Conductor.objects.create(
                user=user, status=status, **conductor_profile_data
            )
            print(conductor)
            group, _ = Group.objects.get_or_create(name="conductores")

            user.groups.add(group)

            return user
        except Exception as e:
            # Si se produce algún error, eliminar el usuario y el conductor creados anteriormente
            if user:
                user.delete()
            if conductor:
                conductor.delete()

            raise serializers.ValidationError(str(e))


class ConductorAdminSerializer(serializers.ModelSerializer):
    conductor = ConductorAdminProfileSerializer(source="conductor_profile", many=False)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "is_active",
            "conductor",
        )
        read_only_fields = [
            "id",
            "username",
            "email",
            "is_active",
            "conductor",
        ]

    @transaction.atomic
    def update(self, instance, validated_data):
        try:
            conductor_profile = instance.conductor_profile
            conductor_profile_data = validated_data.pop("conductor_profile", {})

            conductor_profile.status = conductor_profile_data.get(
                "status", conductor_profile.status
            )

            if conductor_profile.status.name == "ALTA":
                instance.is_active = True
            else:
                instance.is_active = False

            conductor_profile.save()

            instance.save()

            return instance

        except Exception as e:
            raise serializers.ValidationError(str(e))


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = "__all__"


class UbicacionSerializer(serializers.ModelSerializer):
    vehiculo = serializers.CharField(source="vehiculo.__str__", read_only=True)
    conductor = serializers.CharField(
        source="conductor.user.first_name", read_only=True
    )
    estado = serializers.CharField(source="estado.nombre", read_only=True)

    class Meta:
        model = CargaVehiculo
        fields = "__all__"
