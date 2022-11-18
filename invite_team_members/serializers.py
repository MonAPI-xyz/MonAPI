from rest_framework import serializers

class InviteTeamMemberTokenCheckSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=256)
