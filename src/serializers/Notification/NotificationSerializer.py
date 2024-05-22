from rest_framework import serializers
from src.models import Notification
class NotificationSerializer(serializers.ModelSerializer):
    created_at=serializers.DateTimeField(read_only=True)
    updated_at=serializers.DateTimeField(read_only=True)
    class Meta:
        model = Notification
        fields = ['id', 'created_at', 'updated_at', 'title', 'subtitle', 'body', 'parent_id', 'is_read']