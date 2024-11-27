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
        request: Request object with query parameters for "tags" (comma-separated list of tag names),
                 "location_type" (e.g., "country", "city"),
                 and "location_id" (ID of the selected location)

    Returns:
        JsonResponse: JSON response with filtered experiences
    '''
    # Step 1: Get query parameters
    tags = request.GET.get('tags', None)
    location_type = request.GET.get('location_type', None)
    location_id = request.GET.get('location_id', None)
    
    # Start with all experiences
    experiences = Experience.objects.all()
    
    # Step 2: Filter by tags (if provided)
    if tags:
        # Convert comma-separated string into a list
        tag_list = tags.split(',')
        
        # Filter experiences to ensure they have all the selected tags
        for tag_name in tag_list:
            experiences = experiences.filter(tags__name=tag_name)
        
    # Step 3: Filter by location (if provided)
    if location_type and location_id:
        if location_type == 'country':
            # Filter by country (match experiences where the location's country matches the location_id)
            experiences = experiences.filter(location__country_id=location_id)
        elif location_type == 'city':
            # Filter by city (match experiences where the location's city matches the location_id)
            experiences = experiences.filter(location__city_id=location_id)
        
    # Step 4: Sort by average rating and number of ratings
    experiences = experiences.order_by('-average_rating', '-number_of_ratings')
    
    # Step 5: Serialize and return the response
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
