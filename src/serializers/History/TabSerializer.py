from rest_framework import serializers


class TabSerializer(serializers.Serializer):
    card_seri = serializers.CharField(max_length=100, allow_null=True, required=True)
    type = serializers.CharField(max_length=100, allow_null=True, required=True)
    driver_id = serializers.UUIDField(required=True)
    location = serializers.CharField(max_length=100, allow_null=True, required=True)
