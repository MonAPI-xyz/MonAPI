import pytz

from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from datetime import datetime
from django.core.mail import send_mail
from unittest.mock import patch

from forget_password.models import ForgetPasswordToken


def mocked_send_email(*args, **kwargs):
    pass

class RequestForgetPasswordToken(APITestCase):
    test_url = reverse('reset-password-token')
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    mock_current_time = local_timezone.localize(datetime(2022, 9, 20, 10))

    def setUp(self):
        # Mock time function
        timezone.now = lambda: self.mock_current_time

    def test_check_token_if_key_not_exists_then_return_error(self):
        response = self.client.get(self.test_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"key": ["This field is required."]})

    def test_check_token_if_key_exists_but_token_invalid_then_return_error(self):
        response = self.client.get(self.test_url, {
            'key': 'abc'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Invalid token'})
        
    def test_check_token_if_key_exists_and_token_valid_then_return_success(self):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        token = ForgetPasswordToken.objects.create(user=user)
        response = self.client.get(self.test_url, {
            'key': token.key
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'success': True})
        
    def test_request_token_if_parameter_not_exists_then_return_error(self):
        response = self.client.post(self.test_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"email": ["This field is required."]})
        
    def test_request_token_if_user_not_exists_then_return_error(self):
        response = self.client.post(self.test_url, {
            'email': 'invalidmail@admin.com', 
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'User not exists with given email'})
        
    @patch("django.core.mail.send_mail", mocked_send_email)
    def test_request_token_if_user_exists_then_return_success(self):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        response = self.client.post(self.test_url, {
            'email': 'test@test.com', 
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'success': True})
        
    
class ResetPasswordTest(APITestCase):
    test_url = reverse('reset-password')
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    mock_current_time = local_timezone.localize(datetime(2022, 9, 20, 10))

    def setUp(self):
        # Mock time function
        timezone.now = lambda: self.mock_current_time

    def test_if_key_not_exists_then_return_error(self):
        response = self.client.post(self.test_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"password": ["This field is required."], "key": ["This field is required."]})

    def test_if_key_exists_but_token_invalid_then_return_error(self):
        response = self.client.post(self.test_url, {
            'key': 'abc',
            'password': 'Test123486827',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Invalid token'})
        
    def test_if_key_exists_and_token_valid__and_pasword_same_as_old_then_return_error(self):
        user = User.objects.create_user(username='test', email='test@test.com', password='Test123486827')
        token = ForgetPasswordToken.objects.create(user=user)
        response = self.client.post(self.test_url, {
            'key': token.key,
            'password': 'Test123486827',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Please choose password that different from your current password'})
        
    def test_if_key_exists_token_valid_but_invalid_password_then_return_error(self):
        user = User.objects.create_user(username='test', email='test@test.com', password='Test123486827')
        token = ForgetPasswordToken.objects.create(user=user)
        response = self.client.post(self.test_url, {
            'key': token.key,
            'password': 'abc',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"password": [
            "This password is too short. It must contain at least 8 characters.",
            "This password is too common.",
            "The password must contain at least 1 digit, 0-9.",
            "The password must contain at least 1 uppercase letter, A-Z."
        ]})
        
    def test_if_key_exists_and_token_valid_then_return_success(self):
        user = User.objects.create_user(username='test', email='test@test.com', password='Test123486827')
        token = ForgetPasswordToken.objects.create(user=user)
        response = self.client.post(self.test_url, {
            'key': token.key,
            'password': 'Test1234868271',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'success': True})
        
        user = User.objects.get(email='test@test.com')
        self.assertTrue(user.check_password('Test1234868271'))
    
    