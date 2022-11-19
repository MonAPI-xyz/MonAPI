from datetime import timedelta
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import views, status
from rest_framework.response import Response

from invite_team_members.models import InviteTeamMemberToken
from invite_team_members.serializers import (InviteTeamMemberTokenCheckSerializer,
                                             RequestInviteTeamMemberTokenSerializer,
                                             AcceptInviteSerializer,
                                             CancelInviteSerializer)
from login.models import Team, TeamMember

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

            if TeamMember.objects.filter(team=team, user=user).exists():
                verified = TeamMember.objects.get(team=team, user=user).verified
                if verified:
                    return Response({'error': 'User is already in the team'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'error': 'User is already in the process of being invited to the team'},
                                status=status.HTTP_400_BAD_REQUEST)
            invite_token = InviteTeamMemberToken.objects.create(user=user, team=team)

            team_member = TeamMember.objects.create(user=user, team=team, verified=False)

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


class AcceptInviteView(views.APIView):

    def post(self, request, format=None):
        serializer = AcceptInviteSerializer(data=request.data)
        if serializer.is_valid():
            invite_token = InviteTeamMemberToken.objects.filter(
                key=serializer.validated_data['key'],
                created_at__gte=timezone.now() - timedelta(weeks=1)
            )
            if len(invite_token) == 0:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            invite_token = invite_token[0]
            team_target = invite_token.team
            user_target = invite_token.user

            team_member = TeamMember.objects.get(user=user_target, team=team_target)
            if team_member.verified:
                return Response({'error': 'You are already a member of the team'},
                                status=status.HTTP_400_BAD_REQUEST)

            team_member.verified = True
            team_member.save()
            invite_token.delete()
            return Response({'success': True})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CancelInviteView(views.APIView):

    def post(self, request, format=None):
        serializer = CancelInviteSerializer(data=request.data)
        if serializer.is_valid():
            invite_token = InviteTeamMemberToken.objects.filter(
                key=serializer.validated_data['key'],
                created_at__gte=timezone.now() - timedelta(weeks=1)
            )
            if len(invite_token) == 0:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
            invite_token = invite_token[0]
            team_target = invite_token.team
            user_target = invite_token.user

            team_member = TeamMember.objects.get(user=user_target, team=team_target)

            team_member.delete()
            invite_token.delete()
            return Response({'success': True})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

