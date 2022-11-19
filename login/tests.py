from unittest import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from login.models import MonAPIToken, TeamMember, Team, get_file_path

class LoginTest(APITestCase):
    login_url = reverse('login')

    def test_when_non_authenticated_and_login_without_team_then_return_success(self):
        User.objects.create_user(username='test@gmail.com', email='test@gmail.com', password='Test1234')

        request_params = {'email': 'test@gmail.com', 'password': 'Test1234'}
        response = self.client.post(self.login_url, request_params)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response'], 'Sign-in successful.')
        self.assertEqual(response.data['email'], 'test@gmail.com')
        assert(response.data['token'])
        
    def test_when_non_authenticated_and_team_exists_then_return_success(self):
        user = User.objects.create_user(username='test@gmail.com', email='test@gmail.com', password='Test1234')
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)

        request_params = {'email': 'test@gmail.com', 'password': 'Test1234'}
        response = self.client.post(self.login_url, request_params)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response'], 'Sign-in successful.')
        self.assertEqual(response.data['email'], 'test@gmail.com')
        assert(response.data['token'])
        
        tokens = MonAPIToken.objects.all()
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0].team_member, team_member)

    def test_when_non_authenticated_and_login_and_email_or_password_is_invalid(self):
        User.objects.create_user(username='test@gmail.com', email='test@gmail.com', password='Test1234')

        request_params = {'email': 'test@gmail.com', 'password': 'test456'}
        response = self.client.post(self.login_url, request_params)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['response'], 'Invalid email or password.')
    
    def test_not_fill_both_email_and_password_and_login(self):
        User.objects.create_user(username='test@gmail.com', email='test@gmail.com', password='Test1234')

        request_params = {'email': '', 'password': ''}
        response = self.client.post(self.login_url, request_params)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['response'], 'Both email and password are required.')        

    def test_not_fill_email_and_login(self):
        User.objects.create_user(username='test@gmail.com', email='test@gmail.com', password='Test1234')

        request_params = {'email': '', 'password': '123213'}
        response = self.client.post(self.login_url, request_params)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['response'], 'Email is required.')        
    
    def test_not_fill_password_and_login(self):
        User.objects.create_user(username='test@gmail.com', email='test@gmail.com', password='Test1234')

        request_params = {'email': 'test@gmail.com', 'password': ''}
        response = self.client.post(self.login_url, request_params)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['response'], 'Password is required.')        
        
        
class LogoutTest(APITestCase):
    logout_url = reverse('auth-logout')

    def test_when_invalid_token_and_logout_then_return_error(self):
        header = {'HTTP_AUTHORIZATION': f"Token abcdefg"}

        response = self.client.post(self.logout_url, **header)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Invalid token.')
        
    def test_when_valid_token_and_logout_then_return_success(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        response = self.client.post(self.logout_url, **header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 'User Logged out successfully')
        self.assertEqual(MonAPIToken.objects.count(), 0)
   
class CurentTeamTest(APITestCase):
    current_team_url = reverse('auth-current-team')

    def test_when_invalid_token_and_current_team_then_return_error(self):
        header = {'HTTP_AUTHORIZATION': f"Token abcdefg"}

        response = self.client.get(self.current_team_url, **header)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Invalid token.')
        
    def test_when_valid_token_and_current_team_then_return_current_team_information(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        response = self.client.get(self.current_team_url, **header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], team.id)
        

class AvailableTeamTest(APITestCase):
    available_team_url = reverse('auth-available-team')

    def test_when_invalid_token_and_available_team_then_return_error(self):
        header = {'HTTP_AUTHORIZATION': f"Token abcdefg"}

        response = self.client.get(self.available_team_url, **header)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Invalid token.')
        
    def test_when_valid_token_and_available_team_then_return_available_team_information(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        response = self.client.get(self.available_team_url, **header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], team.id)


class ChangeTeamTest(APITestCase):
    change_team_url = reverse('auth-change-team')

    def test_when_invalid_token_and_change_team_then_return_error(self):
        header = {'HTTP_AUTHORIZATION': f"Token abcdefg"}

        response = self.client.post(self.change_team_url, **header)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Invalid token.')
        
    def test_when_valid_token_and_no_team_id_then_error(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        response = self.client.post(self.change_team_url, **header)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Team id required')
        
    def test_when_valid_token_and_invalid_team_id_then_error(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_2 = Team.objects.create(name='test team 2')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        payload = {"id": team_2.id}

        response = self.client.post(self.change_team_url, data=payload, **header)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid team id')
        
    def test_when_valid_token_and_valid_team_id_then_success(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_2 = Team.objects.create(name='test team 2')
        team_member = TeamMember.objects.create(team=team, user=user)
        team_member_2 = TeamMember.objects.create(team=team_2, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        payload = {"id": team_2.id}

        response = self.client.post(self.change_team_url, data=payload, **header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(MonAPIToken.objects.get(key=token.key).team_member, team_member_2)
        self.assertEqual(MonAPIToken.objects.get(key=token.key).team, team_2)
   
    
class MonAPITokenAuthenticationTest(APITestCase):
    test_url = "/"

    def test_when_token_not_exists_then_return_invalid_token(self):
        header = {'HTTP_AUTHORIZATION': f"Token abcdefg"}
        
        response = self.client.get(self.test_url, **header)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Invalid token.')
        
    def test_when_user_not_active_then_return_user_inactive(self):
        user = User.objects.create_user(username='test@gmail.com', email='test@gmail.com', password='Test1234')
        user.is_active = False
        user.save()
        
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(user=user, team=team)
        token = MonAPIToken.objects.create(team_member=team_member)
        
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        
        response = self.client.get(self.test_url, **header)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'User inactive or deleted.')
        self.assertEqual(str(token), token.key)
        

class TeamLogoTest(TestCase):
    def test_generate_logo_path_random(self):
        path = get_file_path(None, 'test.png')
        self.assertTrue('teamlogo/' in path)
    
class InviteMemberTest(TestCase):

    def test_when_invited_a_user_is_not_verified(self):
        user = User.objects.create_user(username='test@gmail.com', email='test@gmail.com', password='Test1234')
        user.is_active = False
        user.save()

        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(user=user, team=team)

        self.assertEqual(team_member.verified, False)

class ListMemberTest(APITestCase):
    test_url = reverse('auth-list-member')
    def test_member_list_returns_all_member_of_the_team(self):
        user1 = User.objects.create_user(username="user1@gmail.com", email="user1@gmail.com", password="test1234")
        user2 = User.objects.create_user(username="user2@gmail.com", email="user2@gmail.com", password="test1234")
        team1 = Team.objects.create(name="team 1")
        team2 = Team.objects.create(name="team 2")
        TeamMember.objects.create(user=user1, team=team1, verified=True)
        TeamMember.objects.create(user=user1, team=team2)
        team_member = TeamMember.objects.create(user=user2, team=team2, verified=True)
        team2_token = MonAPIToken.objects.create(team_member = team_member)
        header = {'HTTP_AUTHORIZATION': f'Token {team2_token.key}'}
        response = self.client.post(self.test_url, {
            'id': team2.id
        }, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_member_on_non_existent_team_should_return_error(self):
        user1 = User.objects.create_user(username="user1@gmail.com", email="user1@gmail.com", password="test1234")
        team1 = Team.objects.create(name="team 1")
        team_member = TeamMember.objects.create(user=user1, team=team1, verified=True)
        team_token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f'Token {team_token.key}'}
        response = self.client.post(self.test_url, {
            'id': -1
        }, **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Invalid team id'})

    def test_list_member_requires_id(self):
        user1 = User.objects.create_user(username="user1@gmail.com", email="user1@gmail.com", password="test1234")
        team1 = Team.objects.create(name="team 1")
        team_member = TeamMember.objects.create(user=user1, team=team1, verified=True)
        team_token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f'Token {team_token.key}'}
        response = self.client.post(self.test_url, {}, **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Team id required'})
