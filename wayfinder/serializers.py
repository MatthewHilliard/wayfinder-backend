from rest_framework import serializers
from cities_light.models import City, Country, Region
from .models import *
from dj_rest_auth.registration.serializers import RegisterSerializer

# NOTE: Each model should have a corresponding serializer to handle validation and
# conversion of incoming data, as well as serializing outgoing data to be
# returned in responses.

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
        
class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(max_length=100)

    def custom_signup(self, request, user):
        # Set the name field explicitly during signup
        user.name = self.validated_data.get('name', '')
        user.save(update_fields=['name'])

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
    image_url = serializers.SerializerMethodField()  # Add custom field for image URL

    class Meta:
        model = Experience
        fields = '__all__'
        
    def get_image_url(self, obj):
        if obj.image:
            return f"{settings.WEBSITE_URL}{obj.image.url}"
        return None
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class RatingSerializer(serializers.ModelSerializer):
    user_info = UserSerializer(source='user', read_only=True)  # Serialize user info for GET requests
    experience_info = ExperienceSerializer(source='experience', read_only=True)  # Serialize experience info for GET requests
    
    class Meta:
        model = Rating
        fields = '__all__'