from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

from .serializers import (
    LoginSerializer,
    LogoutAdminSerializer,
    LogoutSerializer,
    StatusSerializer,
    TipoDocSerializer,
    User,
    OutstandingToken,
    Status,
    TipoDoc,
)
from customConfig.viewsets import CreateOnlyModelViewSet, NewModelViewSet
from rest_framework import viewsets, filters, status

# login y logout


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = User.objects.get(username=request.data.get("username"))
        except Exception as e:
            return Response(
                {"status": False, "message": str(e), "data": {}},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            {
                "status": True,
                "message": "Bienvenido al sistema, " + user.first_name,
                "data": {
                    "email": user.email,
                    "name": user.first_name,
                    "tokens": serializer.validated_data,
                },
            },
            status=status.HTTP_200_OK,
        )


class LogoutAdminViewSet(CreateOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = LogoutAdminSerializer

    def create(self, request, *args, **kwargs):
        user = (
            super(LogoutAdminViewSet, self)
            .create(request, *args, **kwargs)
            .data.get("data")
        )
        return Response(
            {
                "status": True,
                "message": "Se cerraron todas las sesiones del usuario: "
                + str(user.get("username")),
                "data": {},
            }
        )


class LogoutViewSet(CreateOnlyModelViewSet):
    queryset = OutstandingToken.objects.all()
    serializer_class = LogoutSerializer

    def create(self, request, *args, **kwargs):
        super(LogoutViewSet, self).create(request, *args, **kwargs)
        if request.data.get("all"):
            message = "Se cerraron todas las sesiones"
        else:
            message = "Se cerró la sesión exitosamente"
        return Response(
            {
                "status": True,
                "message": message,
                "data": {},
            }
        )


# estatus y tipo doc


class StatusClienteViewSet(NewModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class TipoDocViewSet(NewModelViewSet):
    queryset = TipoDoc.objects.all()
    serializer_class = TipoDocSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
