from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from wayfinder.models import Tag
from wayfinder.serializers import TagSerializer
from rest_framework.permissions import AllowAny

'''--- GET REQUESTS ---'''

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny]) 
def get_tags(request):
    '''
    Get all tags from the database, sorted by name.

    Parameters:
        request: Request object

    Returns:
        JsonResponse: JSON response with all tags sorted by name
    '''
    tags = Tag.objects.all().order_by('name')
    serializer = TagSerializer(tags, many=True)
    return JsonResponse({'data': serializer.data})
