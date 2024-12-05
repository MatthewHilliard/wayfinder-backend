from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.shortcuts import get_object_or_404
from wayfinder.models import Tip
from cities_light.models import Country, City
from wayfinder.serializers import TipSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

'''--- POST REQUESTS ---'''

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def create_tip(request):
    """
    Create a new tip given the required fields.

    Steps:
    1. Ensure the user is authenticated.
    2. Extract required fields from the request.
    3. Validate required fields (content, location_type, location_id).
    4. Get the location (city/country) or throw a 404 if not found.
    5. Create a new Tip object.
    6. Serialize and return the created Tip object.
    """
    # Step 1: Ensure the user is authenticated
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'You must be authenticated to perform this action.'}, status=401)

    # Step 2: Extract data from the request
    data = request.data
    content = data.get('content')
    location_type = data.get('location_type')
    location_id = data.get('location_id')

    # Step 3: Validate required fields
    if not content or not isinstance(content, str) or not content.strip():
        return JsonResponse(
            {'error': 'Content is required.'},
            status=HTTP_400_BAD_REQUEST
        )

    if not location_type or not location_id:
        return JsonResponse(
            {'error': 'Both location_type and location_id are required.'},
            status=HTTP_400_BAD_REQUEST
        )

    # Step 4: Get the city/country or throw 404 if not found
    country = None
    city = None

    if location_type == 'country':
        country = get_object_or_404(Country, id=location_id)
    elif location_type == 'city':
        city = get_object_or_404(City, id=location_id)
        country = city.country  # Assign the associated country from the city

    # Step 5: Create a new Tip object
    tip = Tip.objects.create(
        content=content,
        country=country,
        city=city,
        creator=user
    )

    # Step 6: Serialize and return the created Tip object
    serializer = TipSerializer(tip)
    return JsonResponse({'data': serializer.data}, status=HTTP_201_CREATED)

'''--- GET REQUESTS ---'''

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_tips_with_filters(request):
    '''
    Get all tips from the database with filters.

    Parameters:
        request: Request object with query parameters for "location_type" (e.g., "country", "city"),
                 and "location_id" (ID of the selected location)

    Returns:
        JsonResponse: JSON response with filtered tips
    '''
    # Step 1: Get query parameters
    location_type = request.GET.get('location_type', None)
    location_id = request.GET.get('location_id', None)
    
    # Start with all tips
    tips = Tip.objects.all()
    
    # Step 2: Filter by location (if provided)
    if location_type and location_id:
        if location_type == 'country':
            # Filter by country (match tips where the location's country matches the location_id)
            tips = tips.filter(country=location_id)
        elif location_type == 'city':
            # Filter by city (match tips where the location's city matches the location_id)
            tips = tips.filter(city=location_id)
    
    # Step 3: Sort tips by creation date (newest first)
    tips = tips.order_by('-date_posted')
    
    # Step 4: Serialize and return the response
    serializer = TipSerializer(tips, many=True)
    return JsonResponse({'data': serializer.data})

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def get_tips_by_user_id(request, user_id):
    '''
    Get all tips created by a specific user.

    Parameters:
        request: Request object
        user_id: ID of the user

    Returns:
        JsonResponse: JSON response with all tips created by the user
    '''
    tips = Tip.objects.filter(creator=user_id).order_by('-date_posted')
    serializer = TipSerializer(tips, many=True)
    return JsonResponse({'data': serializer.data})
