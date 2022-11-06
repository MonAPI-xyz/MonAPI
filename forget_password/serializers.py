from rest_framework import serializers


class RequestForgetPasswordTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ForgetPasswordTokenCheckSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=256)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)
    key = serializers.CharField(max_length=256)
