# urls/user_urls.py
from django.urls import path
from wayfinder.views import user_views

# URL routes for calls relating to users
urlpatterns = [
    # GET Requests
    path('get_user_by_id/<str:user_id>/', user_views.get_user_by_id, name='get_user_by_id'),
]
