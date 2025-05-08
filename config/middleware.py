from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin


class SessionUserMiddleware(MiddlewareMixin):
    """
    django.contrib.auth.middleware.AuthenticationMiddleware, django.contrib.auth.middleware.RemoteUserMiddleware
    """

    def process_request(self, request: HttpRequest):
        # NOTE: django.contrib.auth.middleware.AuthenticationMiddleware と同様
        if not hasattr(request, "session"):
            raise ImproperlyConfigured(
                "The Django authentication middleware requires session "
                "middleware to be installed. Edit your MIDDLEWARE setting to "
                "insert "
                "'django.contrib.sessions.middleware.SessionMiddleware' before "
                "'django.contrib.auth.middleware.AuthenticationMiddleware'."
            )

        request.session_user = None
        # TODO: request.user へのアクセスを禁止する
