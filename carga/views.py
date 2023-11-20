from customConfig.viewsets import NewModelViewSet, ListUpdateViewSet
from .serializers import (
    CargaSerializer,
    CargaEstadoSerializer,
    AnularCargaSerializer,
)
from .models import Carga, EstadoCarga
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class CargaViewSet(NewModelViewSet):
    """
    API endpoint that allows carga to be viewed or edited.
    """

    queryset = Carga.objects.all()
    serializer_class = CargaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["descripcion"]
    filterset_fields = ["cliente"]


class AnularCargaViewSet(ListUpdateViewSet):
    queryset = Carga.objects.all()
    serializer_class = AnularCargaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["cliente"]

    def get_queryset(self):
        estado, _ = EstadoCarga.objects.get_or_create(nombre="PENDIENTE DE ATENCIÓN")
        return Carga.objects.filter(estado=estado)


class CargaEstadoViewSet(ListUpdateViewSet):
    """
    API endpoint that allows updating or listing estatus of  Carga model.
    """

    queryset = Carga.objects.all()
    serializer_class = CargaEstadoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["fecha_hora"]
