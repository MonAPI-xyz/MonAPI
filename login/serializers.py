from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import serializers

class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password',]
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True}
        }

    def validate_attribute(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        response = ""
        if not email and not password:
            response = 'Both email and password are required.'
            raise serializers.ValidationError({'response': response}, code='authorization')
        elif not email:
            response = 'Email is required.'
            raise serializers.ValidationError({'response': response}, code='authorization')
        elif not password:
            response = 'Password is required.'
            raise serializers.ValidationError({'response': response}, code='authorization')

        

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'),
                            username=email, email=email, password=password)
        if not user:
            response = 'Invalid email or password.'
            raise serializers.ValidationError({'response':response}, code='authorization')
        
        attrs['user'] = user
        return attrs