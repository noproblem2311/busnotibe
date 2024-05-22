from rest_framework import serializers
from src.models.Admin import Admin


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'