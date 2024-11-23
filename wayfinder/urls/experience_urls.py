# urls/experience_urls.py
from django.urls import path
from wayfinder.views import experience_views

# URL routes for calls relating to experiences
urlpatterns = [
    # POST Requests
    
    # GET Requests
    path('get_experiences/', experience_views.get_experiences, name='get_experiences'),
    path('get_experience_by_id/<str:experience_id>/', experience_views.get_experience_by_id, name='get_experience_by_id'),
]
