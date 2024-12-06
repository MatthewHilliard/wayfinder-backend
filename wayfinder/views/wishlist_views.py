from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from wayfinder.models import Experience, Wishlist, WishlistItem
from wayfinder.serializers import WishlistSerializer, WishlistItemSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def create_wishlist(request):
    """
    Creates a new wishlist for a specific user, ensuring the user is authenticated.
    """
    # Get request data
    user_id = request.data.get('user_id')
    title = request.data.get('title')

    # Get the authenticated user
    user = request.user

    # Ensure the authenticated user is creating their own wishlists
    if str(user.id) != str(user_id):
        return JsonResponse({'error': 'You are not authorized to access this resource.'}, status=403)

    # Create a new Wishlist
    wishlist = Wishlist.objects.create(user=user, title=title)
    serializer = WishlistSerializer(wishlist)

    return JsonResponse({"data": serializer.data}, status=201)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def create_wishlist_item(request, wishlist_id): 
    """
    Creates a new wishlist item for a specific wishlist, ensuring the user is authenticated and the wishlist belongs to the user.
    """   
    # Get user_id and experience_id from request data
    user_id = request.data.get('user_id')
    experience_id = request.data.get('experience_id')

    # Get the authenticated user
    user = request.user
    
    # Ensure the authenticated user is accessing their own wishlists
    if str(user.id) != str(user_id):
        return JsonResponse({'error': 'You are not authorized to access this resource.'}, status=403)

    # Validate that the wishlist belongs to the authenticated user
    wishlist = get_object_or_404(Wishlist, wishlist_id=wishlist_id, user=user)

    # Validate that the experience_id is provided
    if not experience_id:
        return JsonResponse({'error': 'Experience ID is required'}, status=400)

    # Validate that the experience exists
    experience = get_object_or_404(Experience, experience_id=experience_id)

    # Check if the item already exists in the wishlist
    if WishlistItem.objects.filter(wishlist=wishlist, experience=experience).exists():
        return JsonResponse({'error': 'This experience is already in the wishlist'}, status=400)

    # Create a new WishlistItem
    wishlist_item = WishlistItem.objects.create(wishlist=wishlist, experience=experience)
    serializer = WishlistItemSerializer(wishlist_item)

    return JsonResponse({"data": serializer.data}, status=201)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([]) 
def get_user_wishlists(request, user_id):
    """
    Gets all wishlists for a specific user given their user_id.
    """
    user = request.user

    # Ensure the authenticated user is accessing their own wishlists
    if str(user.id) != str(user_id):
        return JsonResponse({'error': 'You are not authorized to access this resource.'}, status=403)

    # Fetch wishlists for the authenticated user
    wishlists = Wishlist.objects.filter(user=user)
    serializer = WishlistSerializer(wishlists, many=True)
    return JsonResponse({"data": serializer.data}, status=200)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([])
def get_wishlist_items(request, wishlist_id):
    user = request.user # Get the authenticated user
    
    # Fetch the wishlist
    wishlist = get_object_or_404(Wishlist, wishlist_id=wishlist_id, user=user)

    # Fetch wishlists for the authenticated user
    wishlist_items = WishlistItem.objects.filter(wishlist=wishlist)
    serializer = WishlistItemSerializer(wishlist_items, many=True)
    
    return JsonResponse({"data": serializer.data}, status=200)
