from customConfig.viewsets import NewModelViewSet
from .models import EstadoPago, Pago
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import EstadoPagoSerializer, PagoSerializer


class EstadoPagoViewSet(NewModelViewSet):
    """
    API endpoint that allows estado pago to be viewed or edited.
    """

    queryset = EstadoPago.objects.all()
    serializer_class = EstadoPagoSerializer


class PagoViewSet(NewModelViewSet):
    """
    API endpoint that allows pago to be viewed or edited.
    """

    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["carga"]
