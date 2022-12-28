from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class RequestForgetPasswordTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ForgetPasswordTokenCheckSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=256)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)
    key = serializers.CharField(max_length=256)
    
    def validate_password(self, password):
        try:
            validate_password(password)
        except ValidationError as exc:
            raise exc
        return password
