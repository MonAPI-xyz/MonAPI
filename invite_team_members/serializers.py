from rest_framework import serializers


class InviteTeamMemberTokenCheckSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=256)


class RequestInviteTeamMemberTokenSerializer(serializers.Serializer):
    sender_id = serializers.IntegerField()
    team_id = serializers.IntegerField()
    invited_email = serializers.EmailField()


class AcceptInviteSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=256)


class CancelInviteSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    team_id = serializers.IntegerField()
    key = serializers.CharField(max_length=256)
