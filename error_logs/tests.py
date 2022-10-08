import pytz
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from apimonitor.models import APIMonitor, APIMonitorResult

class ListErrorLogs(APITestCase):
  url = reverse('error-logs-list')
  local_timezone = pytz.timezone(settings.TIME_ZONE)
  mock_current_time = local_timezone.localize(datetime(2022, 9, 20, 10))

  def setUp(self):
    # Mock time function
    timezone.now = lambda: self.mock_current_time

  def test_when_non_authenticated_then_return_unauthorized(self):
    response = self.client.get(self.url, format='json')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEqual(response.data, {
        "detail": "Authentication credentials were not provided."
    })

  def test_when_authenticated_and_empty_data_then_empty_error_logs_success(self):
    # Create dummy user and authenticate
    user = User.objects.create_user(username='test', email='test@test.com', password='test123')
    token = Token.objects.create(user=user)
    header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

    response = self.client.get(self.url, format='json', **header)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data, [])
  
  def test_when_authenticated_and_data_are_exists_then_view_error_logs_list_success(self):
    # Create dummy user and authenticate
    user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
    token = Token.objects.create(user=user)
    header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

    monitor = APIMonitor.objects.create(
      user=user,
      name='Test Name',
      method='GET',
      url='Test Path',
      schedule='10MIN',
      body_type='EMPTY',
    )

    APIMonitorResult.objects.create(
        monitor=monitor,
        execution_time=self.mock_current_time,
        date=self.mock_current_time.date(),
        hour=self.mock_current_time.hour,
        minute=self.mock_current_time.minute,
        response_time=100,
        success=False,
        log_response='Log Response',
        log_error='',
    )

    APIMonitorResult.objects.create(
        monitor=monitor,
        execution_time=self.mock_current_time,
        date=self.mock_current_time.date(),
        hour=self.mock_current_time.hour,
        minute=self.mock_current_time.minute,
        response_time=75,
        success=False,
        log_response='',
        log_error='Log Error'
    )

    response = self.client.get(self.url, format='json', **header)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data, [
      {
        "id": 1,
        "monitor": {
            "id": 1,
            "name": "Test Name",
            "method": "GET",
            "url": "Test Path",
            "schedule": "10MIN",
            "body_type": "EMPTY",
            "query_params": [],
            "headers": [],
            "body_form": [],
            "raw_body": None
        },
        "execution_time": "2022-09-20T10:00:00+07:00",
        "date": "2022-09-20",
        "hour": 10,
        "minute": 0,
        "response_time": 100,
        "success": False,
        "log_response": "Log Response",
        "log_error": "",
      },
      {
          "id": 2,
          "monitor": {
              "id": 1,
              "name": "Test Name",
              "method": "GET",
              "url": "Test Path",
              "schedule": "10MIN",
              "body_type": "EMPTY",
              "query_params": [],
              "headers": [],
              "body_form": [],
              "raw_body": None
          },
          "execution_time": "2022-09-20T10:00:00+07:00",
          "date": "2022-09-20",
          "hour": 10,
          "minute": 0,
          "response_time": 75,
          "success": False,
          "log_response": "",
          "log_error": "Log Error",
      },
    ])

  def test_when_authenticated_and_data_are_exists_then_view_error_logs_detail_success(self):
    # Create dummy user and authenticate
    user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
    token = Token.objects.create(user=user)
    header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

    monitor = APIMonitor.objects.create(
      user=user,
      name='Test Name',
      method='GET',
      url='Test Path',
      schedule='10MIN',
      body_type='EMPTY',
    )

    APIMonitorResult.objects.create(
        monitor=monitor,
        execution_time=self.mock_current_time,
        date=self.mock_current_time.date(),
        hour=self.mock_current_time.hour,
        minute=self.mock_current_time.minute,
        response_time=100,
        success=False,
        log_response='Log Response',
        log_error='Log Error',
    )

    APIMonitorResult.objects.create(
        monitor=monitor,
        execution_time=self.mock_current_time,
        date=self.mock_current_time.date(),
        hour=self.mock_current_time.hour,
        minute=self.mock_current_time.minute,
        response_time=75,
        success=False,
        log_response='',
        log_error='Log Error'
    )

    log_id = APIMonitorResult.objects.filter(monitor__user=user, success=False)[:1].get().id
    url = reverse('error-logs-detail', kwargs={'pk': log_id})
    response = self.client.get(url, format='json', **header)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data,
      {
        "id": 1,
        "monitor": {
            "id": 1,
            "name": "Test Name",
            "method": "GET",
            "url": "Test Path",
            "schedule": "10MIN",
            "body_type": "EMPTY",
            "query_params": [],
            "headers": [],
            "body_form": [],
            "raw_body": None
        },
        "execution_time": "2022-09-20T10:00:00+07:00",
        "date": "2022-09-20",
        "hour": 10,
        "minute": 0,
        "response_time": 100,
        "success": False,
        "log_response": "Log Response",
        "log_error": "Log Error",
      }
    )
