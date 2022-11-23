from rest_framework import serializers
from login.models import Team, TeamMember
from django.contrib.auth.models import User


class TeamUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username', 
            'email', 
            'first_name', 
            'last_name',
        ]

class TeamMemberSerializers(serializers.ModelSerializer):
    user = TeamUserSerializers()
    class Meta:        
        model = TeamMember
        fields = [
            'team', 
            'user',
            'verified',
        ]

class TeamManagementSerializers(serializers.ModelSerializer):
    teammember = TeamMemberSerializers(many=True)
    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'logo',
            'description',
            'teammember',
        ]




