from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.view_mixin import BaseViewMixin
from login.serializers import SessionSerializer


class LoginView(BaseViewMixin, APIView):
    @method_decorator(csrf_protect)
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user, backend="common.backends.DemoBackend")
            return Response({"message": "Login successful"})
        return Response({"error": "Invalid credentials"}, status=400)


class LogoutView(BaseViewMixin, APIView):
    @method_decorator(csrf_protect)
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"})


class SessionView(BaseViewMixin, APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response(
            SessionSerializer(
                {
                    "user": request.user if request.user.is_authenticated else None,
                    "csrf_token": get_token(request),
                }
            ).data,
            status=status.HTTP_200_OK,
        )
