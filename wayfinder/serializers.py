from rest_framework import serializers
from cities_light.models import City, Country, Region
from .models import *
from dj_rest_auth.registration.serializers import RegisterSerializer

"""--- Auth Serializers ---"""

class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=100)
    location_type = serializers.CharField(max_length=50, required=True)
    location_id = serializers.IntegerField(required=True)

    def custom_signup(self, request, user):
        # Set the name field explicitly during signup
        user.name = self.validated_data.get('name', '')
        
        # Initialize location fields
        user.country = None
        user.city = None
        
        # Extract location data from the request
        location_type = self.validated_data.get('location_type', '').strip()
        location_id = self.validated_data.get('location_id')
        
        # Match the location type and ID
        if location_type and location_id:
            if location_type == 'country':
                country = Country.objects.filter(id=location_id).first()
                if country:
                    user.country = country
            elif location_type == 'city':
                city = City.objects.filter(id=location_id).first()
                if city:
                    user.city = city
                    user.country = city.country
        
        # Save user with updated fields
        user.save(update_fields=["name", "country", "city"])
        
"""--- Django Cities Light Serializers ---"""

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']  # Include relevant city fields
        
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name']  # Include relevant region fields

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']  # Include relevant country fields
        
"""--- Application Serializers ---"""
        
class UserSerializer(serializers.ModelSerializer):
    country_info = CountrySerializer(source='country', read_only=True)  # Serialize country info for GET requests
    city_info = CitySerializer(source='city', read_only=True)  # Serialize city info for GET requests
    profile_picture_url = serializers.SerializerMethodField()  # Add custom field for profile picture URL
    
    class Meta:
        model = User
        fields = '__all__'
        
    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            return f"{settings.WEBSITE_URL}{obj.profile_picture.url}"
        return None

class LocationSerializer(serializers.ModelSerializer):
    city_info = CitySerializer(source='city', read_only=True)  # Serialize city info for GET requests
    region_info = RegionSerializer(source='region', read_only=True)  # Serialize region info for GET requests
    country_info = CountrySerializer(source='country', read_only=True)  # Serialize country info for GET requests
    
    class Meta:
        model = Location
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ExperienceSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)  # Serialize related tags for GET requests
    location_info = LocationSerializer(source='location', read_only=True)  # Serialize related location for GET requests
    creator_info = UserSerializer(source='creator')  # Add custom field for creator info
    image_url = serializers.SerializerMethodField()  # Add custom field for image URL

    class Meta:
        model = Experience
        fields = '__all__'
        
    def get_image_url(self, obj):
        if obj.image:
            return f"{settings.WEBSITE_URL}{obj.image.url}"
        return None
        
class RatingSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user', read_only=True)  # Serialize user info for GET requests
    experience_info = ExperienceSerializer(source='experience', read_only=True)  # Serialize experience info for GET requests
    
    class Meta:
        model = Rating
        fields = '__all__'
        
class WishlistSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user', read_only=True)  # Serialize user info for GET requests
    
    class Meta:
        model = Wishlist
        fields = '__all__'
        
class WishlistItemSerializer(serializers.ModelSerializer):
    experience_info = ExperienceSerializer(source='experience', read_only=True)  # Serialize experience info for GET requests
    
    class Meta:
        model = WishlistItem
        fields = '__all__'
        
class TipSerializer(serializers.ModelSerializer):
    creator_info = UserSerializer(source='creator', read_only=True)  # Serialize creator info for GET requests
    country_info = CountrySerializer(source='country', read_only=True)  # Serialize country info for GET requests
    city_info = CitySerializer(source='city', read_only=True)  # Serialize city info for GET requests
    
    class Meta:
        model = Tip
        fields = '__all__'
