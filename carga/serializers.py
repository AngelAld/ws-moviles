from rest_framework import serializers
from .models import Carga


class CargaSerializer(serializers.ModelSerializer):
    """
    Serializer for the Carga model.
    """

    class Meta:
        model = Carga
        fields = "__all__"
        depth = 2
