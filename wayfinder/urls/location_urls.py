# urls/location_urls.py
from django.urls import path
from wayfinder.views import location_views

# URL routes for calls relating to tags
urlpatterns = [
    # GET Requests
    path('city_search/', location_views.city_search, name='city_search'),
]
