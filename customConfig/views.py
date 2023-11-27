from .viewsets import NewModelViewSet
from .models import Config
from .serializers import ConfigSerializer


class ConfigViewSet(NewModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    http_method_names = ["get", "post", "delete", "put"]
