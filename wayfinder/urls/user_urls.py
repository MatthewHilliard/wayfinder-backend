"""
Author: Matthew Hilliard
Email: mch2003@bu.edu
Description: This module defines URL routes for user-related operations, 
including retrieving user details by ID and updating user information. 
These routes map to the corresponding views in the `user_views` module.
"""

from django.urls import path
from wayfinder.views import user_views

# URL routes for calls relating to users
urlpatterns = [
    # GET Requests
    path('get_user_by_id/<str:user_id>/', user_views.get_user_by_id, name='get_user_by_id'),
    
    # PUT Requests
    path('update_user/<str:user_id>/', user_views.update_user, name='update_user'),
]
