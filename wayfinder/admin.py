"""
Author: Matthew Hilliard
Email: mch2003@bu.edu
Description: This module registers the application's models (Location, User, Experience, Tip, 
Wishlist, WishlistItem, Rating, and Tag) with the Django admin site, enabling their management 
through the admin interface.
"""

from django.contrib import admin

from .models import Location, User, Experience, Tip, Wishlist, WishlistItem, Rating, Tag

'''Registering the models with the admin site'''
admin.site.register(Location)
admin.site.register(User)
admin.site.register(Experience)
admin.site.register(Tip)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)
admin.site.register(Rating)
admin.site.register(Tag)