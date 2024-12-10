"""
Author: Matthew Hilliard
Email: mch2003@bu.edu
Description: This module defines URL routes for tip-related operations, 
including creating tips, retrieving tips with filters, and retrieving tips 
created by a specific user. These routes map to the corresponding views in 
the `tip_views` module.
"""

from django.urls import path
from wayfinder.views import tip_views

# URL routes for calls relating to tips
urlpatterns = [
    # POST Requests
    path('create_tip/', tip_views.create_tip, name='create_tip'),
    
    # GET Requests
    path('get_tips_with_filters/', tip_views.get_tips_with_filters, name='get_tips_with_filters'),
    path('get_tips_by_user_id/<str:user_id>/', tip_views.get_tips_by_user_id, name='get_tips_by_user_id'),
]
