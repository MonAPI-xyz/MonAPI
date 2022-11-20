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
        team_member = TeamMember.objects.create(user=user, team=team)
        inviteToken = InviteTeamMemberToken.objects.create(team_member=team_member)
        self.assertEqual(InviteTeamMemberToken.objects.all().count(), 1)

class RequestInviteTeamMemberTokenViewTest(APITestCase):
    test_url = reverse('invite-member-token')
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    mock_current_time = local_timezone.localize(datetime(2022, 9, 20, 10))

    def setUp(self):
        timezone.now = lambda: self.mock_current_time
        self.default_user = User.objects.create_user(username='default user', email='test@gmail.com', password='test1234')
        self.default_team = Team.objects.create(name='default team')
        self.default_team_member = TeamMember.objects.create(team=self.default_team, user=self.default_user, verified=True)
        self.default_token = MonAPIToken.objects.create(team_member=self.default_team_member)
        self.default_header = {'HTTP_AUTHORIZATION': f"Token {self.default_token.key}"}
        self.default_invite_token = InviteTeamMemberToken.objects.create(team_member=self.default_team_member)

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
        self.assertEqual(len(response.data), 3)

    def test_request_invite_token_but_invited_user_does_not_exist(self):
        response = self.client.post(self.test_url, {
            'sender_id': self.default_user.id,
            'invited_email': 'invalid@gmail.com',
            'team_id': -1
        }, format='json', **self.default_header)
        self.assertEqual(response.data, {'error': 'User not exists with given email'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_invite_token_but_team_does_not_exist(self):
        response = self.client.post(self.test_url, {
            'sender_id': self.default_user.id,
            'invited_email': self.default_user.email,
            'team_id': 1798471298
        }, format='json', **self.default_header)
        self.assertEqual(response.data, {'error': 'Team not exists with given id'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_invite_token_and_everything_valid_but_user_is_already_in_team(self):
        already_verified = User.objects.create_user(username='new', email='new@gmail.com', password='new12345')
        TeamMember.objects.create(user=already_verified, team=self.default_team, verified=False)
        response = self.client.post(self.test_url, {
            'sender_id': self.default_user.id,
            'invited_email': already_verified.email,
            'team_id': self.default_team.id
        }, format='json', **self.default_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'User is already in the process of being invited to the team'})

    @patch("django.core.mail.send_mail", mocked_send_email)
    def test_request_invite_token_and_everything_valid_but_user_is_invited_twice(self):
        invited_user = User.objects.create_user(username='new user', email='new_user@gmail.com', password='test1234')
        response = self.client.post(self.test_url, {
            'sender_id': self.default_user.id,
            'invited_email': invited_user.email,
            'team_id': self.default_team.id
        }, format='json', **self.default_header)
        # User is invited and is added to the team as unverified user
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'success': True})
        self.assertEqual(TeamMember.objects.filter(team=self.default_team).count(), 2)
        self.assertEqual(TeamMember.objects.get(user=invited_user, team=self.default_team).verified, False)

        # User is invited again
        response = self.client.post(self.test_url, {
            'sender_id': self.default_user.id,
            'invited_email': invited_user.email,
            'team_id': self.default_team.id
        }, format='json', **self.default_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'User is already in the process of being invited to the team'})
        self.assertEqual(TeamMember.objects.filter(team=self.default_team).count(), 2)

    def test_request_invite_to_an_already_verified_team_member(self):
        response = self.client.post(self.test_url, {
            'sender_id': self.default_user.id,
            'invited_email': self.default_user.email,
            'team_id': self.default_team.id
        }, format='json', **self.default_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'User is already in the team'})


class AcceptInviteViewTest(APITestCase):
    test_url = reverse('accept-invite')
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    mock_current_time = local_timezone.localize(datetime(2022, 9, 20, 10))

    def setUp(self):
        timezone.now = lambda: self.mock_current_time
        self.default_user = User.objects.create_user(username='default user', email='test@gmail.com',
                                                     password='test1234')
        self.default_team = Team.objects.create(name='default team')
        self.default_team_member = TeamMember.objects.create(team=self.default_team, user=self.default_user, verified=True)
        self.default_token = MonAPIToken.objects.create(team_member=self.default_team_member)
        self.default_header = {'HTTP_AUTHORIZATION': f"Token {self.default_token.key}"}
        self.default_invite_token = InviteTeamMemberToken.objects.create(team_member=self.default_team_member)

    def test_frontend_sends_no_data(self):
        response = self.client.post(self.test_url, {}, format='json', **self.default_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"key": ["This field is required."]})

    def test_invite_already_verified_user(self):
        response = self.client.post(self.test_url, {
            'key': self.default_invite_token.key
        }, format='json', **self.default_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'You are already a member of the team'})

    @patch("django.core.mail.send_mail", mocked_send_email)
    def test_frontend_sends_unused_token_and_try_reusing_same_token(self):
        invited_user = User.objects.create_user(username='new user', email='new_user@gmail.com', password='test1234')
        response = self.client.post(reverse('invite-member-token'), {
            'sender_id': self.default_user.id,
            'invited_email': invited_user.email,
            'team_id': self.default_team.id
        }, format='json', **self.default_header)
        # User is invited and is added to the team as unverified user
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'success': True})
        self.assertEqual(TeamMember.objects.filter(team=self.default_team).count(), 2)

        team_member = TeamMember.objects.get(user=invited_user, team=self.default_team)
        invite_token = InviteTeamMemberToken.objects.get(team_member=team_member)
        invite_token_key = invite_token.key
        response = self.client.post(self.test_url, {
            'key': invite_token_key
        }, format='json', **self.default_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'success': True})
        self.assertEqual(InviteTeamMemberToken.objects.all().count(), 1)

        # Reusing same token
        invite_token_key = invite_token.key
        response = self.client.post(self.test_url, {
            'key': invite_token_key
        }, format='json', **self.default_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Invalid token'})
        self.assertEqual(InviteTeamMemberToken.objects.all().count(), 1)


class CancelInviteViewTest(APITestCase):
    test_url = reverse('cancel-invite')
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    mock_current_time = local_timezone.localize(datetime(2022, 9, 20, 10))

    def setUp(self):
        timezone.now = lambda: self.mock_current_time
        self.default_user = User.objects.create_user(username='default user', email='test@gmail.com',
                                                     password='test1234')
        self.default_team = Team.objects.create(name='default team')
        self.default_team_member = TeamMember.objects.create(team=self.default_team, user=self.default_user, verified=True)
        self.default_token = MonAPIToken.objects.create(team_member=self.default_team_member)
        self.default_header = {'HTTP_AUTHORIZATION': f"Token {self.default_token.key}"}
        self.default_invite_token = InviteTeamMemberToken.objects.create(team_member=self.default_team_member)

    def test_frontend_send_no_data(self):
        response = self.client.post(self.test_url, format='json', **self.default_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"key": ["This field is required."]})

    def test_frontend_sends_invalid_token(self):
        response = self.client.post(self.test_url, {
            'key': 'invalid'
        }, format='json', **self.default_header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Invalid token'})

    @patch("django.core.mail.send_mail", mocked_send_email)
    def test_request_invite_token_and_then_cancel(self):
        invited_user = User.objects.create_user(username='new user', email='new_user@gmail.com', password='test1234')
        self.client.post(reverse('invite-member-token'), {
            'sender_id': self.default_user.id,
            'invited_email': invited_user.email,
            'team_id': self.default_team.id
        }, format='json', **self.default_header)
        team_member = TeamMember.objects.get(user=invited_user, team=self.default_team)
        invite_token = InviteTeamMemberToken.objects.get(team_member=team_member)
        response = self.client.post(self.test_url, {
            'key': invite_token.key
        }, format='json', **self.default_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'success': True})
        self.assertEqual(TeamMember.objects.all().count(), 1)
        self.assertEqual(InviteTeamMemberToken.objects.all().count(), 1)

