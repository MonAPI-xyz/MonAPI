from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from login.models import MonAPIToken, TeamMember, Team

class LoginTest(APITestCase):
    login_url = reverse('login')

    def test_when_non_authenticated_and_login_then_return_success(self):
        # Create dummy user and authenticate
        User.objects.create_user(username='test@gmail.com', email='test@gmail.com', password='Test1234')

        request_params = {'email': 'test@gmail.com', 'password': 'Test1234'}
        response = self.client.post(self.login_url, request_params)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response'], 'Sign-in successful.')
        self.assertEqual(response.data['email'], 'test@gmail.com')
        assert(response.data['token'])
        
    def test_when_non_authenticated_and_team_exists_then_return_success(self):
        # Create dummy user and authenticate
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
        
    def test_when_non_authenticated_and_team_exists_None_return_success(self):
        # Create dummy user and authenticate
        user = User.objects.create_user(username='test@gmail.com', email='test@gmail.com', password='Test1234')
        team_member = TeamMember.objects.create(user=user)

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
        
        team_member = TeamMember.objects.create(user=user)
        token = MonAPIToken.objects.create(team_member=team_member)
        
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        
        response = self.client.get(self.test_url, **header)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'User inactive or deleted.')
        self.assertEqual(str(token), token.key)
