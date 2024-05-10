from rest_framework import serializers
from src.models import Request

class RequestSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Request
        fields = [
            'id',
            'parent_id',
            'status',
            'admin_id',
            'address',
            'template_id',
            'phone_number',
            'name',
            'email',
            'zip_postal',
            'note',
            'created_at',
            'shipping_by',
            'shipping_code',
            'updated_at',
        ]
