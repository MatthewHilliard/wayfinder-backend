from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from wayfinder.models import Tip
from wayfinder.serializers import TipSerializer
from rest_framework.permissions import AllowAny

'''--- GET REQUESTS ---'''

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
