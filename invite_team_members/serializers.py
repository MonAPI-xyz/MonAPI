from rest_framework import serializers


class InviteTeamMemberTokenCheckSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=256)


class RequestInviteTeamMemberTokenSerializer(serializers.Serializer):
    team_id = serializers.IntegerField()
    invited_email = serializers.EmailField()


class AcceptInviteSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=256)
