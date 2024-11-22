# urls/experience_urls.py
from django.urls import path
from wayfinder.views import experience_views

# URL routes for calls relating to experiences
urlpatterns = [
    # POST Requests
    
    # GET Requests
    path('get_experiences/', experience_views.get_experiences, name='get_experiences'),
]
