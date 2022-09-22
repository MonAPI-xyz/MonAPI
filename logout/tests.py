from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

class ListAPIMonitor(APITestCase):
  logout_url = reverse('logout')

  def test_when_non_authenticated_then_return_unauthorized(self):
    response = self.client.post(self.logout_url)

    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEqual(response.data, {
        "detail": "Authentication credentials were not provided."
    })

  def test_when_authenticated_and_logout_then_return_success(self):
    # Create dummy user and authenticate
    user = User.objects.create_user(username='test', email='test@test.com', password='test123')
    token = Token.objects.create(user=user)

    header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
    response = self.client.post(self.logout_url, **header)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data, 'User Logged out successfully')