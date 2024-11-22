# urls/__init__.py
from django.urls import include, path

# In order to have seperate url files, django requires this file and to import the urls here:
from .experience_urls import urlpatterns as experience_urls
from .tag_urls import urlpatterns as tag_urls

# All URL routes
urlpatterns = [
    path('experiences/', include(experience_urls)),
    path('tags/', include(tag_urls)),
]
