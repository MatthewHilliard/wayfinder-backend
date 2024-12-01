# urls/rating_urls.py
from django.urls import path
from wayfinder.views import rating_views

# URL routes for calls relating to ratings
urlpatterns = [
    # POST Requests
    path('create_rating/', rating_views.create_rating, name='create_rating'),
    
    # GET Requests
    path('get_experience_ratings/<str:experience_id>/', rating_views.get_experience_ratings, name='get_experience_ratings'),
]
