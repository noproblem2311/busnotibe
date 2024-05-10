from rest_framework import serializers
from src.models import Template

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = [
            'id',
            'name',
            'image',
            'price',
        ]
        