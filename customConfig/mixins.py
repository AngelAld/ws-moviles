from rest_framework.response import Response
from rest_framework import status, serializers, mixins
from django.db.models.deletion import ProtectedError


class SuccessResponseMixin:
    def render_success(self, data, message):
        if not data:
            return Response(
                {"status": False, "message": "No hay elementos", "data": data}
            )
        return Response({"status": True, "message": message, "data": data})


class ErrorResponseMixin:
    def handle_error(self, exc):
        if isinstance(exc, serializers.ValidationError):
            return Response(
                {"status": False, "message": "Error de validación", "data": exc.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if isinstance(exc, ProtectedError):
            protected_elements = [
                {"name": str(protected_object)}
                for protected_object in exc.protected_objects
            ]
            return Response(
                {
                    "status": False,
                    "message": "No se puede eliminar, hay registros Asociados",
                    "data": protected_elements,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"status": False, "message": "Ocurrió un error", "data": str(exc)},
            status=status.HTTP_400_BAD_REQUEST,
        )


# List Mixin
class ListResponseMixin(
    SuccessResponseMixin, ErrorResponseMixin, mixins.ListModelMixin
):
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return self.render_success(serializer.data, "Listado correcto")
        except Exception as e:
            return self.handle_error(e)


# Retrieve Mixin
class RetrieveResponseMixin(
    SuccessResponseMixin, ErrorResponseMixin, mixins.RetrieveModelMixin
):
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return self.render_success(serializer.data, "Consulta correcta")
        except Exception as e:
            return self.handle_error(e)


# Create Mixin
class CreateResponseMixin(
    SuccessResponseMixin, ErrorResponseMixin, mixins.CreateModelMixin
):
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return self.render_success(serializer.data, "Creación correcta")
        except Exception as e:
            return self.handle_error(e)


class UpdateResponseMixin(
    SuccessResponseMixin, ErrorResponseMixin, mixins.UpdateModelMixin
):
    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop("partial", False)
            instance = self.get_object()
            serializer = self.get_serializer(
                instance, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, "_prefetched_objects_cache", None):
                instance._prefetched_objects_cache = {}

            return self.render_success(serializer.data, "Actualización correcta")
        except Exception as e:
            return self.handle_error(e)


# Delete Mixin
class DeleteResponseMixin(ErrorResponseMixin, mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)

            return Response(
                {"status": True, "message": "Eliminado correctamente", "data": {}}
            )
        except Exception as e:
            return self.handle_error(e)
