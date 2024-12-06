from dj_rest_auth.registration.views import RegisterView
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from wayfinder.serializers import CustomRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.views import LoginView

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

    def perform_create(self, serializer):
        try:
            return super().perform_create(serializer)
        except IntegrityError:
            raise ValidationError({"email": ["A user is already registered with this email address."]})

class CustomLoginView(LoginView):
    def get_response(self):
        response = super().get_response()
        refresh = RefreshToken.for_user(self.user)
        response.data["refresh"] = str(refresh)
        return response