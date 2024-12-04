# urls/wishlist_urls.py
from django.urls import path
from wayfinder.views import wishlist_views

# URL routes for calls relating to wishlists
urlpatterns = [
    # GET Requests
    path('get_user_wishlists/<str:user_id>', wishlist_views.get_user_wishlists, name='get_user_wishlists'),
]
