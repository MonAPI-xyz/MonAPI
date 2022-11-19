import pytz

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from rest_framework import status
from rest_framework.test import APITestCase

from invite_team_members.models import InviteTeamMemberToken
from login.models import Team, TeamMember, MonAPIToken
# Create your tests here.
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
