from customConfig.viewsets import (
    CreateOnlyModelViewSet,
    NewModelViewSet,
    NoCreateViewSet,
    AdminViewSet,
)
from customConfig.permissions import IsAdminOrReadOnly
from .models import User, Vehiculo
from .serializers import (
    ConductorSerializer,
    ConductorAdminSerializer,
    VehiculoSerializer,
    UbicacionSerializer,
    CargaVehiculo,
    EstadoVehiculo,
)
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication


class ConductorRegisterView(NewModelViewSet):
    """
    View para registrar un conductor
    """

    queryset = User.objects.all()
    serializer_class = ConductorSerializer
    http_method_names = ["post"]


class ConductorViewSet(NewModelViewSet):
    """
    ViewSet para los conductors ya registrados
    """

    queryset = User.objects.all()
    serializer_class = ConductorSerializer
    http_method_names = ["get", "put", "delete"]

    def get_queryset(self):
        return User.objects.filter(conductor_profile__isnull=False)


class ConductorAdminViewSet(NewModelViewSet):
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
    http_method_names = ["get", "put", "delete"]

    def get_queryset(self):
        return User.objects.filter(conductor_profile__isnull=False)


class VehiculoViewSet(NewModelViewSet):
    """
    ViewSet para los vehiculos
    """

    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    http_method_names = ["post", "get", "put", "delete"]


class UbicacionViewSet(NewModelViewSet):
    """
    ViewSet para las ubicaciones
    """

    queryset = CargaVehiculo.objects.all()
    serializer_class = UbicacionSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        estado_asignado = EstadoVehiculo.objects.get(nombre="VEHICULO ASIGNADO")
        estado_finalizado = EstadoVehiculo.objects.get(nombre="FINALIZADO")

        return CargaVehiculo.objects.exclude(
            estado__in=[estado_asignado, estado_finalizado]
        )
