"""
Author: Matthew Hilliard
Email: mch2003@bu.edu
Description: This module defines URL routes for authentication-related operations, 
including user registration, login, logout, and token refresh. It integrates custom 
views for registration and login to extend the default behavior provided by Django REST Auth.
"""

from django.urls import path
from dj_rest_auth.jwt_auth import get_refresh_view
from wayfinder.views.auth_views import CustomRegisterView, CustomLoginView
from dj_rest_auth.views import LogoutView

# URL routes for calls relating to authentication
urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
]
