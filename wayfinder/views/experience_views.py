from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import get_object_or_404
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

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_experience_by_id(request, experience_id):
    '''
    Gets an experience from the database by its experience_id.

    Parameters:
        request: Request object
        experience_id: ID of the experience

    Returns:
        JsonResponse: JSON response with the experience
    '''
    experience = get_object_or_404(Experience, experience_id=experience_id)
    serializer = ExperienceSerializer(experience)
    return JsonResponse({'data': serializer.data})
