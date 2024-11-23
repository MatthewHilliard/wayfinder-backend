from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from wayfinder.models import Experience
from wayfinder.serializers import ExperienceSerializer

'''--- GET REQUESTS ---'''

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_experiences(request):
    '''
    Get all experiences from the database.

    Parameters:
        request: Request object

    Returns:
        JsonResponse: JSON response with all experiences
    '''
    experiences = Experience.objects.all()
    serializer = ExperienceSerializer(experiences, many=True)
    return JsonResponse({'data': serializer.data})
