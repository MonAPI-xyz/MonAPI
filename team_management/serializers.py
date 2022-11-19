from rest_framework import serializers
from login.models import Team, TeamMember
from django.contrib.auth.models import User


class TeamUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 
            'email', 
            'first_name', 
            'last_name'
        ]

class TeamMemberSerializers(serializers.ModelSerializer):
    class Meta:
        user = TeamUserSerializers()
        model = TeamMember
        fields = [
            'team', 
            'user'
        ]

class TeamManagementSerializers(serializers.ModelSerializer):
    class Meta:
        teammember = TeamMemberSerializers(many=True)
        model = Team
        fields = [
            'id',
            'name',
            'logo',
            'description',
            'teammember'
        ]




