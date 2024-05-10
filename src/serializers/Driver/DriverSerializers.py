from rest_framework import serializers
from src.models.Driver import Driver

class DriverSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Driver
        fields = ['id', 'user_name', 'email', 'avatar', 'date_of_birth', 'company', 'license', 'bus_number', 'language', 'created_at', 'updated_at', 'phone_number']
