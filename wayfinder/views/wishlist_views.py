from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from wayfinder.models import Wishlist
from wayfinder.serializers import WishlistSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([]) 
def get_user_wishlists(request, user_id):
    user = request.user

    # Ensure the authenticated user is accessing their own wishlists
    if str(user.id) != str(user_id):
        return JsonResponse({'error': 'You are not authorized to access this resource.'}, status=403)

    # Fetch wishlists for the authenticated user
    wishlists = Wishlist.objects.filter(user=user)
    serializer = WishlistSerializer(wishlists, many=True)
    return JsonResponse({"data": serializer.data})