from customConfig.viewsets import (
    CreateOnlyModelViewSet,
    NewModelViewSet,
    NoCreateViewSet,
    AdminViewSet,
)
from customConfig.permissions import IsAdminOrReadOnly
from .models import User
from .serializers import ClienteSerializer, ClienteAdminSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication


class ClienteRegisterView(CreateOnlyModelViewSet):
    """
    View para registrar un cliente
    """

    queryset = User.objects.all()
    serializer_class = ClienteSerializer


class ClienteViewSet(NoCreateViewSet):
    """
    ViewSet para los clientes ya registrados
    """

    queryset = User.objects.all()
    serializer_class = ClienteSerializer

    def get_queryset(self):
        return User.objects.filter(cliente_profile__isnull=False)


class ClienteAdminViewSet(AdminViewSet):
    """
    ViewSet de clientes para los administradores
    """

    queryset = User.objects.all()
    serializer_class = ClienteAdminSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["cliente_profile__name_rs", "cliente_profile__doc"]
    filterset_fields = ["cliente_profile__doc_type", "cliente_profile__status"]
    # permission_classes = [IsAdminOrReadOnly]
    # authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return User.objects.filter(cliente_profile__isnull=False)
