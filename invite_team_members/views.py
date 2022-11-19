from datetime import timedelta
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import views, status
from rest_framework.response import Response

from invite_team_members.models import InviteTeamMemberToken
from invite_team_members.serializers import InviteTeamMemberTokenCheckSerializer, RequestInviteTeamMemberTokenSerializer
from login.models import Team

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

    def post(self, request, format=None):
        serializer = RequestInviteTeamMemberTokenSerializer(data=request.data)
        if serializer.is_valid():
            users = User.objects.filter(email=serializer.validated_data['invited_email'])
            if len(users) == 0:
                return Response({'error': 'User not exists with given email'}, status=status.HTTP_400_BAD_REQUEST)
            user = users[0]
            if not Team.objects.filter(pk=serializer.validated_data['team_id']).exists():
                return Response({'error': 'Team not exists with given id'}, status=status.HTTP_400_BAD_REQUEST)
            team = Team.objects.get(pk=serializer.validated_data['team_id'])
            invite_token = InviteTeamMemberToken.objects.create(user=user, team=team)

            accept_url = f"{os.environ.get('FRONTEND_URL', '')}/invite-member?key={invite_token.key}"
            email_content = f'''
                        You have been invited to join Team {team.name}.\n
                        Please follow below link to accept the invitation and join the team. \n\n
                        {accept_url}
                        This link is valid for 1 week.
                        '''

            email_content_html = render_to_string('email/accept_invite.html', {
                'team_name': team.name,
                'accept_url': accept_url,
            })

            send_mail(
                f'MonAPI Invitation to Team {team.name}',
                email_content,
                None,
                [user.email],
                html_message=email_content_html,
                fail_silently=False,
            )

            return Response({'success': True})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
