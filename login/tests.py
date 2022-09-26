from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class LoginTest(APITestCase):
    login_url = reverse('login')

    def test_when_non_authenticated_and_login_then_return_success(self):
        # Create dummy user and authenticate
        User.objects.create_user(username='test', email='test@gmail.com', password='test123')

        request_params = {'email': 'test@gmail.com', 'password': 'test123'}
        response = self.client.post(self.login_url, request_params)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response'], 'Sign-in successful')

    def test_when_non_authenticated_and_login_and_email_or_password_is_invalid(self):
        User.objects.create_user(username='test', email='test@gmail.com', password='test123')

        request_params = {'email': 'test@gmail.com', 'password': 'test456'}
        response = self.client.post(self.login_url, request_params)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['response'], 'Sign-in failed')

   
