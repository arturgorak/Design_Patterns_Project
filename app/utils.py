from django.core.exceptions import PermissionDenied


def is_logged_in(request):
    if request.user.is_authenticated:
        return request

    raise PermissionDenied
