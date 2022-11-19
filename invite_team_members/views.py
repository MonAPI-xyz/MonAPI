from datetime import timedelta
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import views, status
from rest_framework.response import Response

from invite_team_members.models import InviteTeamMemberToken
from invite_team_members.serializers import InviteTeamMemberTokenCheckSerializer

import os


class RequestInviteTeamMemberTokenView(views.APIView):

    def get(self, request, format=None):
        serializer = InviteTeamMemberTokenCheckSerializer(data=request.query_params)
        if serializer.is_valid():
            token = InviteTeamMemberToken.objects.filter(
                key=serializer.validated_data['key'],
                created_at__gte=timezone.now() - timedelta(weeks=1)
            )
            if len(token) == 0:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': True})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
