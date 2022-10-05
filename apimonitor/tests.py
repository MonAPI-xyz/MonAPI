import json
import pytz
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from apimonitor.models import APIMonitor, APIMonitorBodyForm, APIMonitorHeader, APIMonitorQueryParam, APIMonitorRawBody, \
    APIMonitorResult


class ListAPIMonitor(APITestCase):
    test_url = reverse('api-monitor-list')
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    mock_current_time = local_timezone.localize(datetime(2022, 9, 20, 10))

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
            hour=self.mock_current_time.hour - 1,
            minute=self.mock_current_time.minute,
            response_time=100,
            success=True,
            log_response='{}'
        )

        APIMonitorResult.objects.create(
            monitor=monitor,
            execution_time=self.mock_current_time,
            date=self.mock_current_time.date(),
            hour=self.mock_current_time.hour - 1,
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
                "last_result": {
                    "date": "2022-09-20",
                    "execution_time": "2022-09-20T10:00:00+07:00",
                    "hour": 9,
                    "id": 4,
                    "log_response": "{}",
                    "minute": 0,
                    "monitor": 1,
                    "response_time": 50,
                    "success": False
                },
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
                "raw_body": [
                    {
                        "body": "Test Body",
                        "id": 1,
                        "monitor": 1
                    }
                ],
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
                "last_result": None,
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
                "raw_body": [
                    {
                        "body": "Test Body",
                        "id": 1,
                        "monitor": 1
                    }
                ],
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

    # PBI-13-delete-api-monitor-backend
    def test_user_can_delete_an_api_monitor(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        # Create an API Monitor object under their account
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
            hour=self.mock_current_time.hour - 1,
            minute=self.mock_current_time.minute,
            response_time=100,
            success=True,
            log_response='{}'
        )

        APIMonitorResult.objects.create(
            monitor=monitor,
            execution_time=self.mock_current_time,
            date=self.mock_current_time.date(),
            hour=self.mock_current_time.hour - 1,
            minute=self.mock_current_time.minute,
            response_time=50,
            success=False,
            log_response='{}'
        )

        # Test object is created
        self.assertEqual(APIMonitor.objects.all().count(), 1)

        # Other user CANNOT delete monitor that is now owned by themself
        # Get the monitor's ID, in this case: delete first created
        target_monitor_id = APIMonitor.objects.filter(user=user)[:1].get().id
        delete_test_path = reverse('api-monitor-detail', kwargs={'pk': target_monitor_id})

        # Object is deleted
        self.client.delete(delete_test_path, format='json', **header)
        self.assertEqual(APIMonitor.objects.all().count(), 0)
        self.assertEqual(APIMonitorResult.objects.all().count(), 0)

    def test_non_owner_cannot_delete_another_owned_api_monitor(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        # Create an API Monitor object under their account
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
            hour=self.mock_current_time.hour - 1,
            minute=self.mock_current_time.minute,
            response_time=100,
            success=True,
            log_response='{}'
        )

        APIMonitorResult.objects.create(
            monitor=monitor,
            execution_time=self.mock_current_time,
            date=self.mock_current_time.date(),
            hour=self.mock_current_time.hour - 1,
            minute=self.mock_current_time.minute,
            response_time=50,
            success=False,
            log_response='{}'
        )

        # Create malicious user
        malicious_user = User.objects.create_user(username="test2@test.com", email="test2@test.com",
                                                  password="Test1234")
        token2 = Token.objects.create(user=malicious_user)
        header2 = {'HTTP_AUTHORIZATION': f"Token {token2.key}"}

        # Get path
        target_monitor_id = APIMonitor.objects.filter(user=user)[:1].get().id
        delete_test_path = reverse('api-monitor-detail', kwargs={'pk': target_monitor_id})

        # Request failed, api monitor is not deleted
        response = self.client.delete(delete_test_path, format='json', **header2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(APIMonitor.objects.all().count(), 1)

    def test_user_can_create_new_api_monitor(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'FORM',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
        monitorbodyform_value = [
            {
                'key': 'key4',
                'value': 'value4'
            },
            {
                'key': 'key5',
                'value': 'value5'
            }
        ]
        monitorrawbody_value = "This doesn't matter since body_type is FORM"

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(APIMonitor.objects.all().count(), 1)

    def test_failed_attempt_because_query_params_doesnt_create_object(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'FORM',
        }

        queryparam_value = [
            {
                'value': 'value1',
                'corrupted': 'corrupted'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
        monitorbodyform_value = [
            {
                'key': 'key4',
                'value': 'value4'
            },
            {
                'key': 'key5',
                'value': 'value5'
            }
        ]
        monitorrawbody_value = "This doesn't matter since body_type is FORM"

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(APIMonitor.objects.all().count(), 0)
        self.assertEqual(response.data['error'], "['Please make sure you submit correct [query params]']")

    def test_failed_attempt_because_headers_doesnt_create_object(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'FORM',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'corrupted_key': 'corrupted',
            'value': 'value3'
        }]
        monitorbodyform_value = [
            {
                'key': 'key4',
                'value': 'value4'
            },
            {
                'key': 'key5',
                'value': 'value5'
            }
        ]
        monitorrawbody_value = "This doesn't matter since body_type is FORM"

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(APIMonitor.objects.all().count(), 0)
        self.assertEqual(APIMonitorQueryParam.objects.all().count(), 0)
        self.assertEqual(response.data['error'], "['Please make sure you submit correct [headers]']")

    def test_failed_attempt_because_body_form_doesnt_create_object(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'FORM',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
        monitorbodyform_value = [
            {
                'key': 'key4',
                'value': 'value4'
            },
            {
                'corrupted_key': 'key5',
                'value': 'value5',
            }
        ]
        monitorrawbody_value = "This doesn't matter since body_type is FORM"

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(APIMonitor.objects.all().count(), 0)
        self.assertEqual(APIMonitorQueryParam.objects.all().count(), 0)
        self.assertEqual(APIMonitorHeader.objects.all().count(), 0)
        self.assertEqual(response.data['error'], "['Please make sure you submit correct [body form]']")

    def test_failed_attempt_because_raw_body_doesnt_create_object(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'RAW',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1',
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
        monitorbodyform_value = "This doesn't matter since body type is RAW"
        monitorrawbody_value = ["Corrupted", "Raw", "Body"]

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(APIMonitor.objects.all().count(), 0)
        self.assertEqual(APIMonitorQueryParam.objects.all().count(), 0)
        self.assertEqual(APIMonitorHeader.objects.all().count(), 0)
        self.assertEqual(response.data['error'], "['Please make sure your [raw body] is a valid string or JSON!']")

    def test_user_can_create_api_monitor_with_raw_body(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'RAW',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1',
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
        monitorbodyform_value = "This doesn't matter since body type is FORM"
        monitorrawbody_value = "Valid raw body"

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(APIMonitor.objects.all().count(), 1)
        self.assertEqual(APIMonitorQueryParam.objects.all().count(), 2)
        self.assertEqual(APIMonitorHeader.objects.all().count(), 1)
        self.assertEqual(APIMonitorBodyForm.objects.all().count(), 0)
        self.assertEqual(APIMonitorRawBody.objects.all().count(), 1)

    def test_bad_monitor_data_shouldnt_be_created(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'RAW',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1',
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
        monitorbodyform_value = "This doesn't matter since body_type is RAW"
        monitorrawbody_value = "Valid raw body"

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            # 'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value,
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "['Please make sure your [name, method, url, schedule, body_type] is valid']")

    def test_query_params_is_not_valid(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'RAW',
        }

        queryparam_value = [
            {
                'key': ['invalid', 'key'],
                'value': 'value1',
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
        monitorbodyform_value = "This doesn't matter since body_type is RAW"
        monitorrawbody_value = "Valid raw body"

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value,
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "['Please make sure your [query params] key and value are valid strings!']")

    def test_header_is_not_valid(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'RAW',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1',
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': ['invalid', 'value']
        }]
        monitorbodyform_value = "This doesn't matter since body_type is RAW"
        monitorrawbody_value = "Valid raw body"

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "['Please make sure your [headers] key and value are valid strings!']")

    def test_body_form_is_not_valid(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'FORM',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
        monitorbodyform_value = [
            {
                'key': ['invalid', 'key'],
                'value': 'value4'
            },
            {
                'key': 'key5',
                'value': 'value5'
            }
        ]
        monitorrawbody_value = "This doesn't matter since body_type is FORM"

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "['Please make sure your [body form] key and value are valid strings!']")
