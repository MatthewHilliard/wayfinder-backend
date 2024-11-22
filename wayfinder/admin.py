from django.contrib import admin

from .models import Location, User, Experience, Tip, Wishlist, WishlistItem, Rating, Tag

admin.site.register(Location)
admin.site.register(User)
admin.site.register(Experience)
admin.site.register(Tip)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)
admin.site.register(Rating)
admin.site.register(Tag)