from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from wayfinder.models import Tag
from wayfinder.serializers import TagSerializer

'''--- GET REQUESTS ---'''

@api_view(['GET'])
@permission_classes([])
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
