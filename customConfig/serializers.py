from .models import Config
from rest_framework import serializers


class ConfigSerializer(serializers.ModelSerializer):
    """
    Serializer for Config model
    """

    class Meta:
        model = Config
        fields = "__all__"
