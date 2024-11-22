from rest_framework import serializers
from .models import *

# NOTE: Each model should have a corresponding serializer to handle validation and
# conversion of incoming data, as well as serializing outgoing data to be
# returned in responses.

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'