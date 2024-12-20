"""
Author: Matthew Hilliard
Email: mch2003@bu.edu
Description: This module defines URL routes for wishlist-related operations, 
including creating wishlists, adding items to wishlists, retrieving all wishlists for a user, 
and retrieving items within a specific wishlist. These routes map to the corresponding views 
in the `wishlist_views` module.
"""

from django.urls import path
from wayfinder.views import wishlist_views

# URL routes for calls relating to wishlists
urlpatterns = [
    # POST Requests
    path('create_wishlist', wishlist_views.create_wishlist, name='create_wishlist'),
    path('create_wishlist_item/<str:wishlist_id>', wishlist_views.create_wishlist_item, name='create_wishlist_item'),
    
    # GET Requests
    path('get_user_wishlists/<str:user_id>', wishlist_views.get_user_wishlists, name='get_user_wishlists'),
    path('get_wishlist_items/<str:wishlist_id>', wishlist_views.get_wishlist_items, name='get_wishlist_items'),
]
