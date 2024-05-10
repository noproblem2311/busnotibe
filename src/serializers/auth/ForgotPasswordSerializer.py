from rest_framework import serializers


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
class ConfirmForgotPasswordSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=2048)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)