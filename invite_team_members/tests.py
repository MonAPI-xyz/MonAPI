import pytz

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from invite_team_members.models import InviteTeamMemberToken
from login.models import Team, TeamMember, MonAPIToken
# Create your tests here.

def mocked_send_email(*args, **kwargs):
    pass

class InviteTeamMemberTokenTest(TestCase):
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    mock_current_time = local_timezone.localize(datetime(2022, 9, 20, 10))

    def setUp(self):
        timezone.now = lambda: self.mock_current_time

    def test_when_created_key_is_made(self):
        user = User.objects.create_user(username='test@gmail.com', email='test@gmail.com', password='Test1234')
        team = Team.objects.create(name="default team")
        inviteToken =  InviteTeamMemberToken.objects.create(user=user, team=team)
        self.assertEqual(InviteTeamMemberToken.objects.all().count(), 1)

class RequestInviteTeamMemberTokenViewTest(APITestCase):
    test_url = reverse('invite-member-token')
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    mock_current_time = local_timezone.localize(datetime(2022, 9, 20, 10))

    def setUp(self):
        timezone.now = lambda: self.mock_current_time
        self.default_user = User.objects.create_user(username='default user', email='test@gmail.com', password='test1234')
        self.default_team = Team.objects.create(name='default team')
        self.default_team_member = TeamMember.objects.create(team=self.default_team, user=self.default_user)
        self.default_token = MonAPIToken.objects.create(team_member=self.default_team_member)
        self.default_header = {'HTTP_AUTHORIZATION': f"Token {self.default_token.key}"}
        self.default_invite_token = InviteTeamMemberToken.objects.create(user=self.default_user, team=self.default_team)

    def test_check_user_must_be_authenthicated_to_get_invite_token(self):
        response = self.client.get(self.test_url, format='json', **self.default_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"key": ["This field is required."]})

    def test_check_if_token_is_given_but_invalid(self):
        response = self.client.get(self.test_url, {
            'key': 'invalid'
        }, format='json', **self.default_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Invalid token'})

    def test_check_token_exist_and_is_valid(self):
        response = self.client.get(self.test_url, {
            'key': self.default_invite_token.key
        }, format='json', **self.default_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'success': True})

    def test_request_invite_token_but_no_param(self):
        response = self.client.post(self.test_url, format='json', **self.default_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(response.data), 2)

    def test_request_invite_token_but_invited_user_does_not_exist(self):
        response = self.client.post(self.test_url, {
            'invited_email': 'invalid@gmail.com',
            'team_id': -1
        }, format='json', **self.default_header)
        self.assertEqual(response.data, {'error': 'User not exists with given email'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_invite_token_but_team_does_not_exist(self):
        response = self.client.post(self.test_url, {
            'invited_email': self.default_user.email,
            'team_id': 1798471298
        }, format='json', **self.default_header)
        self.assertEqual(response.data, {'error': 'Team not exists with given id'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_invite_token_and_everything_valid_but_user_is_already_in_team(self):
        response = self.client.post(self.test_url, {
            'invited_email': self.default_user.email,
            'team_id': self.default_team.id
        }, format='json', **self.default_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'User is already in the process of being invited to the team'})

    @patch("django.core.mail.send_mail", mocked_send_email)
    def test_request_invite_token_and_everything_valid_but_user_is_invited_twice(self):
        invited_user = User.objects.create_user(username='new user', email='new_user@gmail.com', password='test1234')
        response = self.client.post(self.test_url, {
            'invited_email': invited_user.email,
            'team_id': self.default_team.id
        }, format='json', **self.default_header)
        # User is invited and is added to the team as unverified user
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'success': True})
        self.assertEqual(TeamMember.objects.filter(team=self.default_team).count(), 2)

        # User is invited again
        response = self.client.post(self.test_url, {
            'invited_email': invited_user.email,
            'team_id': self.default_team.id
        }, format='json', **self.default_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'User is already in the process of being invited to the team'})
        self.assertEqual(TeamMember.objects.filter(team=self.default_team).count(), 2)
