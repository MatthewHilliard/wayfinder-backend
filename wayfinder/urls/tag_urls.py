"""
Author: Matthew Hilliard
Email: mch2003@bu.edu
Description: This module defines URL routes for tag-related operations, 
including retrieving all tags from the database. These routes map to the corresponding 
views in the `tag_views` module.
"""

from django.urls import path
from wayfinder.views import tag_views

# URL routes for calls relating to tags
urlpatterns = [
    # GET Requests
    path('get_tags/', tag_views.get_tags, name='get_tags'),
]
