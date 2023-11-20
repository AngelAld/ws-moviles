from customConfig.viewsets import NewModelViewSet
from .models import EstadoPago, Pago

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
