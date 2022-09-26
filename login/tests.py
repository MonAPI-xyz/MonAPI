from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class LoginTest(APITestCase):
    login_url = reverse('login')

    def test_when_non_authenticated_and_login_then_return_success(self):
        # Create dummy user and authenticate
        User.objects.create_user(username='test@gmail.com', email='test@gmail.com', password='Test1234')

        request_params = {'email': 'test@gmail.com', 'password': 'Test1234'}
        response = self.client.post(self.login_url, request_params)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response'], 'Sign-in successful.')

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
   
