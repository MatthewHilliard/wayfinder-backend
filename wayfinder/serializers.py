from rest_framework import serializers
from .models import *

# NOTE: Each model should have a corresponding serializer to handle validation and
# conversion of incoming data, as well as serializing outgoing data to be
# returned in responses.
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        
class ExperienceSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)  # Serialize related tags for GET requests
    
    class Meta:
        model = Experience
        fields = '__all__'