from rest_framework import serializers
from src.models.Child import Child

class ChildSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Child
        fields = [
            'id',
            'parent_id',
            'child_name',
            'nickname',
            'gender',
            'date_of_birth',
            'card_number',
            'avatar',
            'school_id',
            'name',
            'created_at',
            'updated_at',
        ]