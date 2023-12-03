from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated


class IsWorkerOrReadOnly(BasePermission):
    """
    The authenticated user is in trabajadores group or is read only
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
            or request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="trabajadores").exists()
        )


class IsAdminOrReadOnly(BasePermission):
    """
    The authenticated user is in staff group or is read only
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
            and request.user.is_authenticated
            or request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )


class IsDriverOrReadOnly(BasePermission):
    """
    The authenticated user is in trabajadores group or is read only
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
            or request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name="conductores").exists()
        )
