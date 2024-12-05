from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import get_object_or_404
from wayfinder.models import Experience, Location
from wayfinder.serializers import ExperienceSerializer
from cities_light.models import Country, Region, City
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework_simplejwt.authentication import JWTAuthentication
from wayfinder.helpers import find_nearest_city
from rest_framework.permissions import AllowAny
from django.db.models import Q
import json

'''--- POST REQUESTS ---'''

@api_view(['POST'])
@authentication_classes([JWTAuthentication])  # Use JWTAuthentication for token-based auth
@permission_classes([]) 
def create_experience(request):
    """
    Create a new experience in the database.

    Steps:
    1. Ensure the user is authenticated.
    2. Extract required and optional fields from the request.
    3. Validate required fields (title, description, latitude, longitude).
    4. Attempt to find the country, region, or city based on the provided data.
       - If a city name is provided, attempt to match by name.
       - If no city is found, attempt to match using latitude and longitude incrementally.
    5. Create or fetch the Location object using the latitude, longitude, and matched data.
    6. Create the Experience object using the authenticated user, Location, and request data.
    7. Attach tags to the Experience if provided.
    8. Serialize and return the created Experience object.
    """
    # Step 1: Ensure the user is authenticated
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'You must be authenticated to perform this action.'}, status=401)

    # Step 2: Extract data from the request
    data = request.data
    title = data.get('title')
    description = data.get('description')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    country_name = data.get('country_name')
    region_name = data.get('region_name')
    city_name = data.get('city_name')
    tags = data.get('tags', [])
    price = data.get('price')
    image = request.FILES.get('image')  # Handle the uploaded image file

    # Step 3: Validate required fields
    if not title or not description or latitude is None or longitude is None:
        return JsonResponse(
            {'error': 'Title, description, latitude, and longitude are required.'},
            status=HTTP_400_BAD_REQUEST
        )
        
    try:
        # Convert latitude and longitude to float
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return JsonResponse(
            {'error': 'Latitude and longitude must be valid floating-point numbers.'},
            status=HTTP_400_BAD_REQUEST
        )
        
    # Parse tags from JSON string to a list
    if tags:
        try:
            tags = json.loads(tags)  # Convert JSON string to Python list
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Tags must be a valid JSON array.'}, status=HTTP_400_BAD_REQUEST)

    # Step 4: Fetch country, region, or city with partial matching
    country = Country.objects.filter(name__icontains=country_name).first() if country_name else None
    region = Region.objects.filter(Q(name__icontains=region_name) & Q(country=country)).first() if region_name else None
    city = City.objects.filter(Q(name__icontains=city_name) & Q(region=region)).first() if city_name else None

    # If no city is found by name, fallback to latitude/longitude incrementally
    if not city:
        city = find_nearest_city(latitude, longitude)

    # Step 5: Create or fetch the Location
    location, _ = Location.objects.get_or_create(
        latitude=latitude,
        longitude=longitude,
        defaults={"country": country, "region": region, "city": city}
    )

    # Step 6: Create the Experience
    experience = Experience.objects.create(
        title=title,
        description=description,
        location=location,
        creator=user,
        price=price,
        image=image
    )

    # Step 7: Attach tags (if provided)
    if tags:
        experience.tags.set(tags)

    # Step 8: Serialize and return the created experience
    serializer = ExperienceSerializer(experience)
    return JsonResponse({'data': serializer.data}, status=HTTP_201_CREATED)

'''--- GET REQUESTS ---'''

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny]) 
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
@permission_classes([AllowAny]) 
def get_experiences_with_filters(request):
    '''
    Get all experiences from the database with filters.

    Parameters:
        request: Request object with query parameters for "tags" (comma-separated list of tag names),
                 "search_query" (search query for title and description),
                 "location_type" (e.g., "country", "city"),
                 and "location_id" (ID of the selected location)

    Returns:
        JsonResponse: JSON response with filtered experiences
    '''
    # Step 1: Get query parameters
    tags = request.GET.get('tags', None)
    search_query = request.GET.get('search_query', None)
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
            
    # Step 3: Filter by search query (if provided)
    if search_query:
        experiences = experiences.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )
        
    # Step 4: Filter by location (if provided)
    if location_type and location_id:
        if location_type == 'country':
            # Filter by country (match experiences where the location's country matches the location_id)
            experiences = experiences.filter(location__country_id=location_id)
        elif location_type == 'city':
            # Filter by city (match experiences where the location's city matches the location_id)
            experiences = experiences.filter(location__city_id=location_id)
        
    # Step 5: Sort by average rating and number of ratings
    experiences = experiences.order_by('-average_rating', '-number_of_ratings')
    
    # Step 6: Serialize and return the response
    serializer = ExperienceSerializer(experiences, many=True)
    return JsonResponse({'data': serializer.data})

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny]) 
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

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_experiences_by_user_id(request, user_id):
    '''
    Get all experiences created by a specific user.

    Parameters:
        request: Request object
        user_id: ID of the user

    Returns:
        JsonResponse: JSON response with all experiences created by the user
    '''
    experiences = Experience.objects.filter(creator=user_id).order_by('-date_posted')
    serializer = ExperienceSerializer(experiences, many=True)
    return JsonResponse({'data': serializer.data})