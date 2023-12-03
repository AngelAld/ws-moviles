from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenObtainSerializer,
)
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import Token
from django.contrib.auth.models import User
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from django.db import transaction
from .models import Status, TipoDoc
from django.utils.translation import gettext_lazy as _

# Logins y logouts


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer, TokenObtainSerializer):
    # Overriding validate function in the TokenObtainSerializer
    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        try:
            user = User.objects.get(username=authenticate_kwargs["username"])
            if not user.is_active:
                self.error_messages["no_active_account"] = _("El usuario esta inactivo")
                raise exceptions.AuthenticationFailed(
                    self.error_messages["no_active_account"],
                    "no_active_account",
                )
        except User.DoesNotExist:
            self.error_messages["no_active_account"] = _("El usuario no existe")
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        self.user = authenticate(**authenticate_kwargs)

        if self.user is None:
            self.error_messages["no_active_account"] = _("Contraseña incorrecta")
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        return super().validate(attrs)


class LogoutAdminSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "user_id")
        read_only_fields = ("id", "username")

    def create(self, validated_data):
        try:
            user_id = validated_data.pop("user_id")
            user = User.objects.get(id=user_id)

            for token in OutstandingToken.objects.filter(user=user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)

            return user
        except Exception as e:
            raise serializers.ValidationError(str(e))


class LogoutSerializer(serializers.ModelSerializer):
    all = serializers.BooleanField(write_only=True, default=False)

    class Meta:
        model = OutstandingToken
        fields = ["token", "all"]

    @transaction.atomic
    def create(self, validated_data):
        try:
            if validated_data.get("all"):
                token_instance = OutstandingToken.objects.get(
                    token=validated_data.get("token")
                )

                user = User.objects.get(id=token_instance.user_id)
                for token in OutstandingToken.objects.filter(user=user):
                    _, _ = BlacklistedToken.objects.get_or_create(token=token)
                    print(token)
                return token_instance
            else:
                token_instance = OutstandingToken.objects.get(
                    token=validated_data.get("token")
                )
                if token_instance:
                    _, _ = BlacklistedToken.objects.get_or_create(token=token_instance)
                return token_instance
        except Exception as e:
            raise serializers.ValidationError(str(e))


# Estatus, Tipo documento


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class TipoDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDoc
        fields = "__all__"
