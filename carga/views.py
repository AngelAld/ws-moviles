from customConfig.viewsets import NewModelViewSet
from .serializers import CargaSerializer
from .models import Carga


class CargaViewSet(NewModelViewSet):
    """
    API endpoint that allows carga to be viewed or edited.
    """

    queryset = Carga.objects.all()
    serializer_class = CargaSerializer
