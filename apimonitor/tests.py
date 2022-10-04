import pytz
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from apimonitor.models import APIMonitor, APIMonitorBodyForm, APIMonitorHeader, APIMonitorQueryParam, APIMonitorRawBody, APIMonitorResult


class ListAPIMonitor(APITestCase):
    test_url = reverse('api-monitor-list')
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    mock_current_time = local_timezone.localize(datetime(2022,9,20,10))
    
    def setUp(self):
        # Mock time function
        timezone.now = lambda: self.mock_current_time
    
    def test_when_non_authenticated_then_return_forbidden(self):
        response = self.client.get(self.test_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {
            "detail": "Authentication credentials were not provided."
        })
    
    def test_when_authenticated_and_empty_monitor_then_return_success_empty_monitor(self):
        # Create dummy user and authenticate
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        
        response = self.client.get(self.test_url, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
        
    def test_when_authenticated_and_non_empty_monitor_then_return_success_with_monitor(self):
        # Create dummy user and authenticate
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        
        monitor = APIMonitor.objects.create(
            user=user,
            name='Test Monitor',
            method='GET',
            url='Test Path',
            schedule='10MIN',
            body_type='FORM',
        )
        
        APIMonitorQueryParam.objects.create(
            monitor=monitor,
            key='Test Key Query',
            value='Test Value Query',
        )
        
        APIMonitorHeader.objects.create(
            monitor=monitor,
            key='Test Key Header',
            value='Test Value Header',
        )
        
        APIMonitorBodyForm.objects.create(
            monitor=monitor,
            key='Test Key Body',
            value='Test Value Body',
        )
        
        APIMonitorRawBody.objects.create(
            monitor=monitor,
            body='Test Body',
        )
        
        APIMonitorResult.objects.create(
            monitor=monitor,
            execution_time=self.mock_current_time,
            date=self.mock_current_time.date(),
            hour=self.mock_current_time.hour,
            minute=self.mock_current_time.minute,
            response_time=100,
            success=True,
            log_response='{}'
        )
        
        APIMonitorResult.objects.create(
            monitor=monitor,
            execution_time=self.mock_current_time,
            date=self.mock_current_time.date(),
            hour=self.mock_current_time.hour,
            minute=self.mock_current_time.minute,
            response_time=75,
            success=True,
            log_response='{}'
        )
        
        APIMonitorResult.objects.create(
            monitor=monitor,
            execution_time=self.mock_current_time,
            date=self.mock_current_time.date(),
            hour=self.mock_current_time.hour-1,
            minute=self.mock_current_time.minute,
            response_time=100,
            success=True,
            log_response='{}'
        )
        
        APIMonitorResult.objects.create(
            monitor=monitor,
            execution_time=self.mock_current_time,
            date=self.mock_current_time.date(),
            hour=self.mock_current_time.hour-1,
            minute=self.mock_current_time.minute,
            response_time=50,
            success=False,
            log_response='{}'
        )
        
        response = self.client.get(self.test_url, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {
                "avg_response_time": 81,
                "body_form": [
                    {
                        "id": 1,
                        "key": "Test Key Body",
                        "monitor": 1,
                        "value": "Test Value Body"
                    }
                ],
                "body_type": "FORM",
                "headers": [
                    {
                        "id": 1,
                        "key": "Test Key Header",
                        "monitor": 1,
                        "value": "Test Value Header"
                    }
                ],
                "id": 1,
                "method": "GET",
                "name": "Test Monitor",
                "query_params": [
                    {
                        "id": 1,
                        "key": "Test Key Query",
                        "monitor": 1,
                        "value": "Test Value Query"
                    }
                ],
                "raw_body": {
                    "body": "Test Body",
                    "id": 1,
                    "monitor": 1
                },
                "schedule": "10MIN",
                "success_rate": "75.0",
                "success_rate_history": [
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 11,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 12,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 13,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 14,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 15,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 16,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 17,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 18,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 19,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 20,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 21,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 22,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 23,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 0,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 1,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 2,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 3,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 4,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 5,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 6,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 7,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 8,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 1,
                        "hour": 9,
                        "minute": 0,
                        "success": 1
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 10,
                        "minute": 0,
                        "success": 2
                    }
                ],
                "url": "Test Path"
            }
        ])
        
    
    def test_when_authenticated_and_empty_monitor_result_then_return_one_hunderd_success_rate(self):
        # Create dummy user and authenticate
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        
        monitor = APIMonitor.objects.create(
            user=user,
            name='Test Monitor',
            method='GET',
            url='Test Path',
            schedule='10MIN',
            body_type='FORM',
        )
        
        APIMonitorQueryParam.objects.create(
            monitor=monitor,
            key='Test Key Query',
            value='Test Value Query',
        )
        
        APIMonitorHeader.objects.create(
            monitor=monitor,
            key='Test Key Header',
            value='Test Value Header',
        )
        
        APIMonitorBodyForm.objects.create(
            monitor=monitor,
            key='Test Key Body',
            value='Test Value Body',
        )
        
        APIMonitorRawBody.objects.create(
            monitor=monitor,
            body='Test Body',
        )
        
        response = self.client.get(self.test_url, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [
            {
                "avg_response_time": 0,
                "body_form": [
                    {
                        "id": 1,
                        "key": "Test Key Body",
                        "monitor": 1,
                        "value": "Test Value Body"
                    }
                ],
                "body_type": "FORM",
                "headers": [
                    {
                        "id": 1,
                        "key": "Test Key Header",
                        "monitor": 1,
                        "value": "Test Value Header"
                    }
                ],
                "id": 1,
                "method": "GET",
                "name": "Test Monitor",
                "query_params": [
                    {
                        "id": 1,
                        "key": "Test Key Query",
                        "monitor": 1,
                        "value": "Test Value Query"
                    }
                ],
                "raw_body": {
                    "body": "Test Body",
                    "id": 1,
                    "monitor": 1
                },
                "schedule": "10MIN",
                "success_rate": "100.0",
                "success_rate_history": [
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 11,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 12,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 13,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 14,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 15,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 16,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 17,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 18,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 19,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 20,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 21,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 22,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-19",
                        "failed": 0,
                        "hour": 23,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 0,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 1,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 2,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 3,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 4,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 5,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 6,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 7,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 8,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 9,
                        "minute": 0,
                        "success": 0
                    },
                    {
                        "date": "2022-09-20",
                        "failed": 0,
                        "hour": 10,
                        "minute": 0,
                        "success": 0
                    }
                ],
                "url": "Test Path"
            }
        ])
