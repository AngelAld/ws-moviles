from customConfig.viewsets import NewModelViewSet
from .models import EstadoPago, Pago
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import EstadoPagoSerializer, PagoSerializer, ConfirmarPagoSerializer


class EstadoPagoViewSet(NewModelViewSet):
    """
    API endpoint that allows estado pago to be viewed or edited.
    """

    queryset = EstadoPago.objects.all()
    serializer_class = EstadoPagoSerializer
    http_method_names = ["get", "post", "put", "delete", "options"]


class PagoViewSet(NewModelViewSet):
    """
    API endpoint that allows pago to be viewed or edited.
    """

    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["carga"]
    http_method_names = ["get", "post", "delete", "options"]


class ConfirmarPagoViewSet(NewModelViewSet):
    """
    API endpoint that allows pago a confirmar
    """

    queryset = Pago.objects.all()
    serializer_class = ConfirmarPagoSerializer
    http_method_names = ["put"]
