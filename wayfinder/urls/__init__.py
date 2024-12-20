"""
Author: Matthew Hilliard
Email: mch2003@bu.edu
Description: This module serves as the main entry point for defining URL routes in the application. 
It consolidates URLs from separate modules, such as `auth_urls`, `experience_urls`, and others, 
into a single list for better organization and scalability. The `urlpatterns` includes routes for 
admin, authentication, experiences, locations, tags, users, ratings, wishlists, and tips.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin

# In order to have seperate url files, django requires this file and to import the urls here:
from .experience_urls import urlpatterns as experience_urls
from .tag_urls import urlpatterns as tag_urls
from .location_urls import urlpatterns as location_urls
from .auth_urls import urlpatterns as auth_urls
from .user_urls import urlpatterns as user_urls
from .rating_urls import urlpatterns as rating_urls
from .wishlist_urls import urlpatterns as wishlist_urls
from .tips_urls import urlpatterns as tips_urls

# All URL routes are defined here
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(auth_urls)),
    path('experiences/', include(experience_urls)),
    path('locations/', include(location_urls)),
    path('tags/', include(tag_urls)),
    path('users/', include(user_urls)),
    path('ratings/', include(rating_urls)),
    path('wishlists/', include(wishlist_urls)),
    path('tips/', include(tips_urls)),
]
