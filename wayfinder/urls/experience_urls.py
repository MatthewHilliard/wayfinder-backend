"""
Author: Matthew Hilliard
Email: mch2003@bu.edu
Description: This module defines URL routes for handling experience-related operations, 
including creating experiences, retrieving all experiences, filtering experiences by criteria, 
and retrieving experiences by ID or user ID. These routes map to the corresponding views in 
the `experience_views` module.
"""

from django.urls import path
from wayfinder.views import experience_views

# URL routes for calls relating to experiences
urlpatterns = [
    # POST Requests
    path('create_experience/', experience_views.create_experience, name='create_experience'),
    
    # GET Requests
    path('get_experiences/', experience_views.get_experiences, name='get_experiences'),
    path('get_experiences_with_filters/', experience_views.get_experiences_with_filters, name='get_experiences_with_filters'),
    path('get_experience_by_id/<str:experience_id>/', experience_views.get_experience_by_id, name='get_experience_by_id'),
    path('get_experiences_by_user_id/<str:user_id>/', experience_views.get_experiences_by_user_id, name='get_experiences_by_user_id'),
]
