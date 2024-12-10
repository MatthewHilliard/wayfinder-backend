"""
Author: Matthew Hilliard
Email: mch2003@bu.edu
Description: This module provides an API view for retrieving all tags. The `get_tags` 
function fetches tags from the database, sorts them alphabetically by name, and returns 
them in a JSON response.
"""

from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from wayfinder.models import Tag
from wayfinder.serializers import TagSerializer
from rest_framework.permissions import AllowAny

"""--- GET REQUESTS ---"""

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny]) 
def get_tags(request):
    """
    Get all tags from the database, sorted by name.

    Parameters:
        request: Request object

    Returns:
        JsonResponse: JSON response with all tags sorted by name
    """
    tags = Tag.objects.all().order_by('name')
    serializer = TagSerializer(tags, many=True)
    return JsonResponse({'data': serializer.data})
