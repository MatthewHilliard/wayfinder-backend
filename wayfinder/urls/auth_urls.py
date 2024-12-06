# urls/auth_urls.py
from django.urls import path
from dj_rest_auth.jwt_auth import get_refresh_view
from wayfinder.views.auth_views import CustomRegisterView, CustomLoginView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView
from rest_framework_simplejwt.views import TokenVerifyView

# URL routes for calls relating to authentication
urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
]
