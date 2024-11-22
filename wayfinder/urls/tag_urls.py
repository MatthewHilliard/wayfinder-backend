# urls/tag_urls.py
from django.urls import path
from wayfinder.views import tag_views

# URL routes for calls relating to tags
urlpatterns = [
    # GET Requests
    path('get_tags/', tag_views.get_tags, name='get_tags'),
]
