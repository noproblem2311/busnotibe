from rest_framework import serializers
from src.models.Company import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name_en', 'name_cn', 'created_at', 'updated_at']
