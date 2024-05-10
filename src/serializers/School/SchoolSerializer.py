from rest_framework import serializers
from src.models.School import School

class SchoolSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = School
        fields = [
            'id',
            'name_en',
            'name_cn'           
        ]