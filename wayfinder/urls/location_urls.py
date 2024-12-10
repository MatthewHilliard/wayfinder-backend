"""
Author: Matthew Hilliard
Email: mch2003@bu.edu
Description: This module defines URL routes for location-related operations, 
including searching for cities and countries based on user queries. These routes 
map to the corresponding views in the `location_views` module.
"""

from django.urls import path
from wayfinder.views import location_views

# URL routes for calls relating to tags
urlpatterns = [
    # GET Requests
    path('city_search/', location_views.city_search, name='city_search'),
]
