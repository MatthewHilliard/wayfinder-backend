# urls/tips_urls.py
from django.urls import path
from wayfinder.views import tip_views

# URL routes for calls relating to tips
urlpatterns = [
    # GET Requests
    path('get_tips_by_user_id/<str:user_id>/', tip_views.get_tips_by_user_id, name='get_tips_by_user_id'),
]
