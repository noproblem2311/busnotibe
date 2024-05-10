from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)
    username = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(max_length=10, allow_null=True, required=False)
    date_of_birth = serializers.DateTimeField(allow_null=True, required=False)

class LoginSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)
    
class ChangePasswordSerializer(serializers.Serializer):
    previous_password = serializers.CharField(max_length=256)
    proposed_password = serializers.CharField(max_length=256)
    
class RespondToNewPasswordChallengeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=2048)
    email = serializers.EmailField()

class ResendConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()