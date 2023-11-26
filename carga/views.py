from customConfig.viewsets import NewModelViewSet
from .serializers import (
    CargaSerializer,
    CargaEstadoSerializer,
    AnularCargaSerializer,
    EstadoSerializer,
)
from .models import Carga, EstadoCarga
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth.models import User, Group

######


class CargaViewSet(NewModelViewSet):
    """
    API endpoint that allows carga to be viewed or edited.
    """

    queryset = Carga.objects.all()
    serializer_class = CargaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["descripcion"]
    filterset_fields = ["cliente"]
    http_method_names = ["get", "post", "delete"]

    # def get_queryset(self):
    #     clientes_group, _ = Group.objects.get_or_create(name="clientes")
    #     return Carga.objects.filter(cliente__groups__in=[clientes_group])


class AnularCargaViewSet(NewModelViewSet):

    """
    API endpoint that allows carga to be canceled if its status is pendiente de atención.
    """

    queryset = Carga.objects.all()
    serializer_class = AnularCargaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["cliente"]
    http_method_names = ["put"]

    # def get_queryset(self):
    #     estado, _ = EstadoCarga.objects.get_or_create(nombre="PENDIENTE DE ATENCIÓN")
    #     return Carga.objects.filter(estado=estado)


class HistorialCargaViewSet(NewModelViewSet):
    """
    API endpoint that allows updating or listing historial of  estatus of  Carga model.
    """

    queryset = Carga.objects.all()
    serializer_class = CargaEstadoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["fecha_hora"]
    http_method_names = ["put", "get"]


class EstadoCargaViewSet(NewModelViewSet):
    """
    API endpoint that allows updating or listing EstatusCarga model.
    """

    queryset = EstadoCarga.objects.all()
    serializer_class = EstadoSerializer
    http_method_names = ["get", "post", "put", "delete"]
