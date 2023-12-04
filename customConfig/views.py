from .viewsets import NewModelViewSet
from .models import Config
from .serializers import ConfigSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication


class ConfigViewSet(NewModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    http_method_names = ["get", "post", "delete", "put"]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
