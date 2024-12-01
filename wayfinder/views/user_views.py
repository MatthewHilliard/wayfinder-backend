from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from wayfinder.models import User
from django.shortcuts import get_object_or_404
from wayfinder.serializers import UserSerializer
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny]) 
def get_user_by_id(request, user_id):
    '''
    Gets an user from the database by its user_id.

    Parameters:
        request: Request object
        user_id: ID of the user

    Returns:
        JsonResponse: JSON response with the user
    '''
    user = get_object_or_404(User, pk=user_id)
    serializer = UserSerializer(user)
    return JsonResponse({'data': serializer.data})