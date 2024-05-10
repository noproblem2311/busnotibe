from rest_framework import serializers
from src.models import Parent

class ParentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Parent
        fields = ['id', 'user_name', 'email', 'avatar', 'date_of_birth', 'language', 'created_at', 'updated_at', 'device']