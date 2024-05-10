from rest_framework import serializers
from django.utils import timezone
from django.db import models
from src.models.History import History


class HistorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    class Meta:
        model = History
        fields = [
            'id',
            'driver_id',
            'child_id',
            'created_at',
            'updated_at',
            'location',
            'type',
        ]
