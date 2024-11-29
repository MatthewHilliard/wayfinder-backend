from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from wayfinder.models import Experience, Location
from wayfinder.serializers import ExperienceSerializer
from cities_light.models import Country, Region, City
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

'''--- POST REQUESTS ---'''
@api_view(['POST'])
@authentication_classes([])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can create experiences
def create_experience(request):
    """
    Create a new experience in the database.
    
    Steps:
    1. Fetch the IDs for the city, region, or country from cities_light models.
    2. Create a Location object if it doesn't exist.
    3. Create an Experience object.
    4. Return the created experience.

    Parameters:
        request: HTTP POST request with required fields:
            - title
            - description
            - city_name (optional)
            - region_name (optional)
            - country_name (optional)
            - latitude (optional, fallback from city/region if not provided)
            - longitude (optional, fallback from city/region if not provided)
            - tags (optional list of tag names)
            - price (optional)
            - start_time (optional)
            - end_time (optional)
            - date (optional)
    
    Returns:
        JsonResponse: JSON response with the created experience or an error message.
    """
    data = request.data
    user = request.user  # Get the authenticated user

    # Step 1: Fetch city, region, or country by name
    country_name = data.get('country_name')
    region_name = data.get('region_name')
    city_name = data.get('city_name')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    country = Country.objects.filter(name__iexact=country_name).first() if country_name else None
    region = Region.objects.filter(name__iexact=region_name, country=country).first() if region_name else None
    city = City.objects.filter(name__iexact=city_name, region=region).first() if city_name else None

    # If no latitude/longitude is provided, use the city's coordinates as fallback
    if not latitude and city:
        latitude = city.latitude
    if not longitude and city:
        longitude = city.longitude

    if not latitude or not longitude:
        return JsonResponse({'error': 'Latitude and longitude could not be determined.'}, status=HTTP_400_BAD_REQUEST)

    # Step 2: Create or fetch the Location
    location = Location.objects.get_or_create(
        latitude=latitude,
        longitude=longitude,
        country=country,
        region=region,
        city=city,
    )

    # Step 3: Validate Experience data
    title = data.get('title')
    description = data.get('description')
    tags = data.get('tags', [])
    price = data.get('price')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    date = data.get('date')

    if not title or not description:
        return JsonResponse({'error': 'Title and description are required.'}, status=HTTP_400_BAD_REQUEST)

    # Step 4: Create the Experience
    experience = Experience.objects.create(
        title=title,
        description=description,
        location=location,
        creator=user,
        price=price,
        start_time=start_time,
        end_time=end_time,
        date=date,
    )

    # Attach tags (if provided)
    if tags:
        experience.tags.set(tags)  # Ensure tags are already created in the database

    # Serialize and return the created experience
    serializer = ExperienceSerializer(experience)
    return JsonResponse({'data': serializer.data}, status=HTTP_201_CREATED)

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
