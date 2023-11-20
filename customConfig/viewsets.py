from .mixins import (
    ListResponseMixin,
    RetrieveResponseMixin,
    CreateResponseMixin,
    UpdateResponseMixin,
    DeleteResponseMixin,
)
from rest_framework.viewsets import GenericViewSet


class WriteOnlyModelViewSet(
    UpdateResponseMixin,
    DeleteResponseMixin,
    GenericViewSet,
):
    pass


class CreateOnlyModelViewSet(
    CreateResponseMixin,
    GenericViewSet,
):
    pass


class AdminViewSet(
    ListResponseMixin,
    RetrieveResponseMixin,
    UpdateResponseMixin,
    DeleteResponseMixin,
    GenericViewSet,
):
    pass


class NewModelViewSet(
    ListResponseMixin,
    RetrieveResponseMixin,
    CreateResponseMixin,
    UpdateResponseMixin,
    DeleteResponseMixin,
    GenericViewSet,
):
    pass


class ListUpdateViewSet(
    ListResponseMixin,
    RetrieveResponseMixin,
    UpdateResponseMixin,
    GenericViewSet,
):
    pass


class NoCreateViewSet(
    ListResponseMixin,
    RetrieveResponseMixin,
    UpdateResponseMixin,
    DeleteResponseMixin,
    GenericViewSet,
):
    pass
