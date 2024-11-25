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
    experiences = Experience.objects.all().order_by('-average_rating', '-number_of_ratings')
    serializer = ExperienceSerializer(experiences, many=True)
    return JsonResponse({'data': serializer.data})

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_experiences_with_filters(request):
    '''
    Get all experiences from the database with filters.

    Parameters:
        request: Request object with a query parameter "tags" (comma-separated list of tag names)

    Returns:
        JsonResponse: JSON response with all experiences
    '''
    # Step 1: Filter based on tags
    # Get tags from query parameters
    tags = request.GET.get('tags', None)
    
    # Start with all experiences
    experiences = Experience.objects.all()
    
    if tags:
        # Convert comma-separated string into a list
        tag_list = tags.split(',')
        
        # Filter experiences by tags
        experiences = experiences.filter(tags__name__in=tag_list).distinct()
        
    # Sort by average rating and number of ratings
    experiences = experiences.order_by('-average_rating', '-number_of_ratings')
    
    # Serialize and return the response
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
