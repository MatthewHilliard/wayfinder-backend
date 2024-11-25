# urls/__init__.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin

# In order to have seperate url files, django requires this file and to import the urls here:
from .experience_urls import urlpatterns as experience_urls
from .tag_urls import urlpatterns as tag_urls
from .location_urls import urlpatterns as location_urls

# All URL routes
urlpatterns = [
    path('admin/', admin.site.urls),
    path('experiences/', include(experience_urls)),
    path('tags/', include(tag_urls)),
    path('locations/', include(location_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
