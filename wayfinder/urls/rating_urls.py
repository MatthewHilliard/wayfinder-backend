"""
Author: Matthew Hilliard
Email: mch2003@bu.edu
Description: This module defines URL routes for rating-related operations, 
including creating a rating for an experience and retrieving all ratings for a 
specific experience. These routes map to the corresponding views in the `rating_views` module.
"""

from django.urls import path
from wayfinder.views import rating_views

# URL routes for calls relating to ratings
urlpatterns = [
    # POST Requests
    path('create_rating/', rating_views.create_rating, name='create_rating'),
    
    # GET Requests
    path('get_experience_ratings/<str:experience_id>/', rating_views.get_experience_ratings, name='get_experience_ratings'),
]
