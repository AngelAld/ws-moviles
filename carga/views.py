from customConfig.viewsets import NewModelViewSet, ListUpdateViewSet
from .serializers import (
    CargaSerializer,
    HistorialEstadoSerializer,
    CargaEstadoSerializer,
)
from .models import Carga, HistorialEstado
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


class CargaEstadoViewSet(ListUpdateViewSet):
    """
    API endpoint that allows updating or listing estatus of  Carga model.
    """

    queryset = Carga.objects.all()
    serializer_class = CargaEstadoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["fecha_hora"]
