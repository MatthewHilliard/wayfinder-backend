from django.http import JsonResponse
from django.shortcuts import get_list_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from django.db.models import F
from wayfinder.models import Experience, Rating
from wayfinder.serializers import RatingSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

'''--- POST REQUESTS ---'''

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def create_rating(request):
    """
    Create a new rating for an experience and update the average rating and number of ratings.

    Steps:
    1. Ensure the user is authenticated.
    2. Extract required fields from the request.
    3. Validate required fields (experience_id, rating_value, comment).
    4. Get the experience or throw 404 if not found.
    5. Create a new Rating object.
    6. Update the experience's average rating and number of ratings.
    7. Serialize and return the created Rating object.
    """
    # Step 1: Ensure the user is authenticated
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'You must be authenticated to perform this action.'}, status=401)

    # Step 2: Extract data from the request
    data = request.data
    experience_id = data.get('experience_id')
    rating_value = data.get('rating_value')
    comment = data.get('comment')

    # Step 3: Validate required fields
    if not experience_id:
        return JsonResponse(
            {'error': 'Experience ID is are required.'},
            status=HTTP_400_BAD_REQUEST
        )
    if comment is None or not isinstance(comment, str) or not comment.strip():
        return JsonResponse(
            {'error': 'A valid comment is required.'},
            status=HTTP_400_BAD_REQUEST
        )

    # Validate and parse rating_value (optional field)
    if rating_value is not None:
        try:
            rating_value = int(rating_value)
            if not (1 <= rating_value <= 5):
                raise ValueError
        except (TypeError, ValueError):
            return JsonResponse(
                {'error': 'Rating value must be an integer between 1 and 5.'},
                status=HTTP_400_BAD_REQUEST
            )

    # Step 4: Get the experience or throw 404 if not found
    experience = get_object_or_404(Experience, experience_id=experience_id)

    # Step 5: Create a new Rating object
    rating = Rating.objects.create(
        user=user,
        experience=experience,
        rating_value=rating_value,
        comment=comment
    )

    # Step 6: Update the experience's average rating and number of ratings
    total_ratings = experience.number_of_ratings
    new_total_ratings = total_ratings + 1
    
    # Update the average rating if a rating value was provided
    if rating_value is not None:
        new_average_rating = ((experience.average_rating * total_ratings) + rating_value) / new_total_ratings
        experience.average_rating = new_average_rating
    
    # Update fields in the database for number of ratings
    experience.number_of_ratings = new_total_ratings
    experience.save()

    # Step 7: Serialize and return the created rating
    serializer = RatingSerializer(rating)
    return JsonResponse({'data': serializer.data}, status=HTTP_201_CREATED)

'''--- GET REQUESTS ---'''

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny]) 
def get_experience_ratings(request, experience_id):
    '''
    Get all ratings for a specific experience, sorted by date (most recent first).

    Parameters:
        request: Request object
        experience_id: The ID of the experience to get ratings for

    Returns:
        JsonResponse: JSON response with all ratings for the experience sorted by date
    '''
    # Get all ratings for the experience sorted by date, throw 404 if none found
    ratings = get_list_or_404(Rating.objects.order_by('-date_posted'), experience_id=experience_id)
    
    # Serialize the ratings and return them in a JSON response
    serializer = RatingSerializer(ratings, many=True)
    return JsonResponse({'data': serializer.data}, status=200)
