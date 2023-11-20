from rest_framework import serializers
from .models import Cliente
from django.contrib.auth.models import User, Group
from django.db import transaction
from usuario.models import Status


class ClienteProfileSerializer(serializers.ModelSerializer):
    docTypeName = serializers.StringRelatedField(source="doc_type")
    statusName = serializers.StringRelatedField(source="status")

    class Meta:
        model = Cliente
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


class ClienteAdminProfileSerializer(serializers.ModelSerializer):
    docTypeName = serializers.StringRelatedField(source="docType")
    statusName = serializers.StringRelatedField(source="status")

    class Meta:
        model = Cliente
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


class ClienteSerializer(serializers.ModelSerializer):
    cliente = ClienteProfileSerializer(source="cliente_profile", many=False)
    name_rs = serializers.CharField(source="first_name")

    class Meta:
        model = User
        fields = (
            "id",
            "name_rs",
            "email",
            "password",
            "is_active",
            "cliente",
        )
        read_only_fields = ("id", "is_active")
        extra_kwargs = {"password": {"write_only": True}}

    @transaction.atomic
    def update(self, instance, validated_data):
        cliente_profile = instance.cliente_profile
        cliente_profile_data = validated_data.pop("cliente_profile", {})

        cliente_profile.doc = cliente_profile_data.get("doc", cliente_profile.doc)
        cliente_profile.address = cliente_profile_data.get(
            "address", cliente_profile.address
        )
        cliente_profile.cel = cliente_profile_data.get("cel", cliente_profile.cel)
        cliente_profile.doc_type = cliente_profile_data.get(
            "doc_type", cliente_profile.doc_type
        )

        cliente_profile.save()

        instance.username = validated_data.get("email", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.set_password(validated_data.get("password", instance.password))
        instance.email = validated_data.get("email", instance.email)
        instance.save()

        return instance

    @transaction.atomic
    def create(self, validated_data):
        try:
            cliente_profile_data = validated_data.pop("cliente_profile", {})
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

            cliente = Cliente.objects.create(
                user=user, status=status, **cliente_profile_data
            )
            print(cliente)
            group, _ = Group.objects.get_or_create(name="clientes")

            user.groups.add(group)

            return user
        except Exception as e:
            # Si se produce algún error, eliminar el usuario y el cliente creados anteriormente
            if user:
                user.delete()
            if cliente:
                cliente.delete()

            raise serializers.ValidationError(str(e))


class ClienteAdminSerializer(serializers.ModelSerializer):
    cliente = ClienteAdminProfileSerializer(source="cliente_profile", many=False)
    name_rs = serializers.CharField(source="first_name", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "name_rs",
            "email",
            "is_active",
            "cliente",
        )
        read_only_fields = [
            "id",
            "name_rs",
            "email",
            "is_active",
            "cliente",
        ]

    @transaction.atomic
    def update(self, instance, validated_data):
        try:
            cliente_profile = instance.cliente_profile
            cliente_profile_data = validated_data.pop("cliente_profile", {})

            cliente_profile.status = cliente_profile_data.get(
                "status", cliente_profile.status
            )

            if cliente_profile.status.name == "ALTA":
                instance.is_active = True
            else:
                instance.is_active = False

            cliente_profile.save()

            instance.save()

            return instance

        except Exception as e:
            raise serializers.ValidationError(str(e))
