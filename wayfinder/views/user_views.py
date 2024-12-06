from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from wayfinder.models import User
from django.shortcuts import get_object_or_404
from wayfinder.serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny]) 
def get_user_by_id(request, user_id):
    """
    Gets an user from the database by its user_id.

    Parameters:
        request: Request object
        user_id: ID of the user

    Returns:
        JsonResponse: JSON response with the user
    """
    user = get_object_or_404(User, pk=user_id)
    serializer = UserSerializer(user)
    return JsonResponse({'data': serializer.data})

@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def update_user(request, user_id):
    """
    Updates an user in the database by their user_id.

    Parameters:
        request: Request object
        user_id: ID of the user
    """
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'error': 'You can only update your own user.'}, status=403)
    
    # Extract data from the request
    data = request.data
    user.name = data.get('name', user.name)
    profile_picture = request.FILES.get('profile_picture')
    
    # Update the profile picture if it was provided
    if profile_picture:
        user.profile_picture = profile_picture   
         
    # Save the updated user
    user.save()
    
    # Serialize and return the response
    serializer = UserSerializer(user)
    return JsonResponse({'data': serializer.data})
    