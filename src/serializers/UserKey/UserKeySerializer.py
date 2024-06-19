from rest_framework import serializers
from src.models import UserKey

class UserKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserKey
        fields = '__all__'