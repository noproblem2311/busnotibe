from rest_framework import serializers
from src.models import Parent

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['id', 'user_name', 'email', 'password', 'avatar', 'date_of_birth']