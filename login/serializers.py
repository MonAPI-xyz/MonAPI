from rest_framework import serializers
from login.models import Team, TeamMember

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

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

        
class TeamSerializers(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            'id',
            'name',
        ]


class TeamMemberSerializers(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    class Meta:
        model = TeamMember
        fields = [
            'user',
            'username',
            'verified',
        ]
