from customConfig.viewsets import (
    CreateOnlyModelViewSet,
    NewModelViewSet,
    NoCreateViewSet,
    AdminViewSet,
)
from customConfig.permissions import IsAdminOrReadOnly
from .models import User
from .serializers import ConductorSerializer, ConductorAdminSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication


class ConductorRegisterView(CreateOnlyModelViewSet):
    """
    View para registrar un conductor
    """

    queryset = User.objects.all()
    serializer_class = ConductorSerializer


class ConductorViewSet(NoCreateViewSet):
    """
    ViewSet para los conductors ya registrados
    """

    queryset = User.objects.all()
    serializer_class = ConductorSerializer

    def get_queryset(self):
        return User.objects.filter(conductor_profile__isnull=False)


class ConductorAdminViewSet(AdminViewSet):
    """
    ViewSet de conductores para los administradores
    """

    queryset = User.objects.all()
    serializer_class = ConductorAdminSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["conductor_profile__name_rs", "conductor_profile__doc"]
    filterset_fields = ["conductor_profile__doc_type", "conductor_profile__status"]
    # permission_classes = [IsAdminOrReadOnly]
    # authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return User.objects.filter(conductor_profile__isnull=False)
