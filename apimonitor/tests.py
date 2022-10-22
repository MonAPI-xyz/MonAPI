import pytz
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .models import APIMonitor, APIMonitorBodyForm, APIMonitorHeader, APIMonitorQueryParam, APIMonitorRawBody, \
    APIMonitorResult

class DetailListAPIMonitor(APITestCase):
    test_url = reverse('api-monitor-detail',args=[1])
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    mock_current_time = local_timezone.localize(datetime(2022, 9, 20, 10))

    def setUp(self):
        # Mock time function
        timezone.now = lambda: self.mock_current_time

    def init_for_test_retrieve_without_result(self, range_schedule):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        monitor = APIMonitor.objects.create(
            user=user,
            name='Test Monitor',
            method='GET',
            url='Test Path',
            schedule=range_schedule,
            body_type='FORM',
        )

        response = self.client.get(self.test_url,{"range":range_schedule},format="json",**header)
        return response

    def init_for_test_retrieve_with_result(self, range_schedule):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        monitor = APIMonitor.objects.create(
            user=user,
            name='Test Monitor',
            method='GET',
            url='Test Path',
            schedule=range_schedule,
            body_type='FORM',
        )

        APIMonitorResult.objects.create(
            monitor=monitor,
            execution_time=self.mock_current_time,
            response_time=100,
            success=True,
            status_code=200,
            log_response='{}'
        )

        response = self.client.get(self.test_url,{"range":range_schedule},format="json",**header)
        return response

    def test_retrieve_30_min_with_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_with_result(self,"30MIN")

        self.assertEqual(response.data,{"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "30MIN", "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body": 
None, "success_rate": [{"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:31:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:31:00+07:00", "end_time": "2022-09-20T09:32:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:32:00+07:00", "end_time": "2022-09-20T09:33:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:33:00+07:00", "end_time": "2022-09-20T09:34:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:34:00+07:00", "end_time": 
"2022-09-20T09:35:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:35:00+07:00", "end_time": "2022-09-20T09:36:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:36:00+07:00", "end_time": "2022-09-20T09:37:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:37:00+07:00", "end_time": "2022-09-20T09:38:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:38:00+07:00", "end_time": "2022-09-20T09:39:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:39:00+07:00", "end_time": "2022-09-20T09:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:41:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:41:00+07:00", "end_time": "2022-09-20T09:42:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:42:00+07:00", "end_time": "2022-09-20T09:43:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:43:00+07:00", "end_time": "2022-09-20T09:44:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:44:00+07:00", "end_time": "2022-09-20T09:45:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:45:00+07:00", "end_time": "2022-09-20T09:46:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:46:00+07:00", "end_time": "2022-09-20T09:47:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:47:00+07:00", "end_time": "2022-09-20T09:48:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:48:00+07:00", "end_time": "2022-09-20T09:49:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:49:00+07:00", "end_time": "2022-09-20T09:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:51:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:51:00+07:00", "end_time": "2022-09-20T09:52:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:52:00+07:00", "end_time": "2022-09-20T09:53:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:53:00+07:00", "end_time": "2022-09-20T09:54:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:54:00+07:00", "end_time": "2022-09-20T09:55:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:55:00+07:00", "end_time": "2022-09-20T09:56:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:56:00+07:00", "end_time": "2022-09-20T09:57:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:57:00+07:00", "end_time": "2022-09-20T09:58:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:58:00+07:00", "end_time": "2022-09-20T09:59:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:59:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "success": 1, "failed": 0}], "response_time": [{"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:31:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:31:00+07:00", "end_time": "2022-09-20T09:32:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:32:00+07:00", "end_time": "2022-09-20T09:33:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:33:00+07:00", "end_time": "2022-09-20T09:34:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:34:00+07:00", "end_time": "2022-09-20T09:35:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:35:00+07:00", "end_time": "2022-09-20T09:36:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:36:00+07:00", "end_time": "2022-09-20T09:37:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:37:00+07:00", "end_time": "2022-09-20T09:38:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:38:00+07:00", "end_time": "2022-09-20T09:39:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:39:00+07:00", "end_time": "2022-09-20T09:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:41:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:41:00+07:00", "end_time": "2022-09-20T09:42:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:42:00+07:00", "end_time": "2022-09-20T09:43:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:43:00+07:00", "end_time": "2022-09-20T09:44:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:44:00+07:00", "end_time": "2022-09-20T09:45:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:45:00+07:00", "end_time": "2022-09-20T09:46:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:46:00+07:00", "end_time": "2022-09-20T09:47:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:47:00+07:00", "end_time": "2022-09-20T09:48:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:48:00+07:00", "end_time": "2022-09-20T09:49:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:49:00+07:00", "end_time": "2022-09-20T09:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:51:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:51:00+07:00", "end_time": "2022-09-20T09:52:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:52:00+07:00", "end_time": "2022-09-20T09:53:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:53:00+07:00", "end_time": "2022-09-20T09:54:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:54:00+07:00", "end_time": "2022-09-20T09:55:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:55:00+07:00", "end_time": "2022-09-20T09:56:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:56:00+07:00", "end_time": "2022-09-20T09:57:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:57:00+07:00", "end_time": "2022-09-20T09:58:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:58:00+07:00", "end_time": "2022-09-20T09:59:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:59:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "avg": 100}]})

    def test_retrieve_30_min_without_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_without_result(self,"30MIN")   # print(json.dumps(response.data))

        self.assertEqual(response.data,{"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "30MIN", "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body": 
None, "success_rate": [{"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:31:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:31:00+07:00", "end_time": "2022-09-20T09:32:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:32:00+07:00", "end_time": "2022-09-20T09:33:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:33:00+07:00", "end_time": "2022-09-20T09:34:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:34:00+07:00", "end_time": 
"2022-09-20T09:35:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:35:00+07:00", "end_time": "2022-09-20T09:36:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:36:00+07:00", "end_time": "2022-09-20T09:37:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:37:00+07:00", "end_time": "2022-09-20T09:38:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:38:00+07:00", "end_time": "2022-09-20T09:39:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:39:00+07:00", "end_time": "2022-09-20T09:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:41:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:41:00+07:00", "end_time": "2022-09-20T09:42:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:42:00+07:00", "end_time": "2022-09-20T09:43:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:43:00+07:00", "end_time": "2022-09-20T09:44:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:44:00+07:00", "end_time": "2022-09-20T09:45:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:45:00+07:00", "end_time": "2022-09-20T09:46:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:46:00+07:00", "end_time": "2022-09-20T09:47:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:47:00+07:00", "end_time": "2022-09-20T09:48:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:48:00+07:00", "end_time": "2022-09-20T09:49:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:49:00+07:00", "end_time": "2022-09-20T09:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:51:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:51:00+07:00", "end_time": "2022-09-20T09:52:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:52:00+07:00", "end_time": "2022-09-20T09:53:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:53:00+07:00", "end_time": "2022-09-20T09:54:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:54:00+07:00", "end_time": "2022-09-20T09:55:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:55:00+07:00", "end_time": "2022-09-20T09:56:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:56:00+07:00", "end_time": "2022-09-20T09:57:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:57:00+07:00", "end_time": "2022-09-20T09:58:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:58:00+07:00", "end_time": "2022-09-20T09:59:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:59:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "success": 0, "failed": 0}], "response_time": [{"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:31:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:31:00+07:00", "end_time": "2022-09-20T09:32:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:32:00+07:00", "end_time": "2022-09-20T09:33:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:33:00+07:00", "end_time": "2022-09-20T09:34:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:34:00+07:00", "end_time": "2022-09-20T09:35:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:35:00+07:00", "end_time": "2022-09-20T09:36:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:36:00+07:00", "end_time": "2022-09-20T09:37:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:37:00+07:00", "end_time": "2022-09-20T09:38:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:38:00+07:00", "end_time": "2022-09-20T09:39:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:39:00+07:00", "end_time": "2022-09-20T09:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:41:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:41:00+07:00", "end_time": "2022-09-20T09:42:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:42:00+07:00", "end_time": "2022-09-20T09:43:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:43:00+07:00", "end_time": "2022-09-20T09:44:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:44:00+07:00", "end_time": "2022-09-20T09:45:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:45:00+07:00", "end_time": "2022-09-20T09:46:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:46:00+07:00", "end_time": "2022-09-20T09:47:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:47:00+07:00", "end_time": "2022-09-20T09:48:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:48:00+07:00", "end_time": "2022-09-20T09:49:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:49:00+07:00", "end_time": "2022-09-20T09:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:51:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:51:00+07:00", "end_time": "2022-09-20T09:52:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:52:00+07:00", "end_time": "2022-09-20T09:53:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:53:00+07:00", "end_time": "2022-09-20T09:54:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:54:00+07:00", "end_time": "2022-09-20T09:55:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:55:00+07:00", "end_time": "2022-09-20T09:56:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:56:00+07:00", "end_time": "2022-09-20T09:57:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:57:00+07:00", "end_time": "2022-09-20T09:58:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:58:00+07:00", "end_time": "2022-09-20T09:59:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:59:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "avg": 0}]})
    
    
    def test_retrieve_1_hour_with_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_with_result(self,"60MIN")

        self.assertEqual(response.data,{"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "60MIN", "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body": None, "success_rate": [{"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:02:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:02:00+07:00", "end_time": "2022-09-20T09:04:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:04:00+07:00", "end_time": "2022-09-20T09:06:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:06:00+07:00", "end_time": "2022-09-20T09:08:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:08:00+07:00", "end_time": "2022-09-20T09:10:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:12:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:12:00+07:00", "end_time": "2022-09-20T09:14:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:14:00+07:00", "end_time": "2022-09-20T09:16:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:16:00+07:00", "end_time": "2022-09-20T09:18:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:18:00+07:00", "end_time": "2022-09-20T09:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:22:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:22:00+07:00", "end_time": "2022-09-20T09:24:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:24:00+07:00", "end_time": "2022-09-20T09:26:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:26:00+07:00", "end_time": "2022-09-20T09:28:00+07:00", "success": 0, 
"failed": 0}, {"start_time": "2022-09-20T09:28:00+07:00", "end_time": "2022-09-20T09:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:32:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:32:00+07:00", "end_time": "2022-09-20T09:34:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:34:00+07:00", "end_time": "2022-09-20T09:36:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:36:00+07:00", "end_time": "2022-09-20T09:38:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:38:00+07:00", "end_time": "2022-09-20T09:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:42:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:42:00+07:00", "end_time": "2022-09-20T09:44:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:44:00+07:00", "end_time": "2022-09-20T09:46:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:46:00+07:00", "end_time": "2022-09-20T09:48:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:48:00+07:00", "end_time": "2022-09-20T09:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:52:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:52:00+07:00", "end_time": "2022-09-20T09:54:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:54:00+07:00", "end_time": "2022-09-20T09:56:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:56:00+07:00", "end_time": "2022-09-20T09:58:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:58:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "success": 1, "failed": 0}], "response_time": [{"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:02:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:02:00+07:00", "end_time": "2022-09-20T09:04:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:04:00+07:00", "end_time": "2022-09-20T09:06:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:06:00+07:00", "end_time": "2022-09-20T09:08:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:08:00+07:00", "end_time": "2022-09-20T09:10:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:12:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:12:00+07:00", "end_time": "2022-09-20T09:14:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:14:00+07:00", "end_time": "2022-09-20T09:16:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:16:00+07:00", "end_time": "2022-09-20T09:18:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:18:00+07:00", "end_time": "2022-09-20T09:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:22:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:22:00+07:00", "end_time": "2022-09-20T09:24:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:24:00+07:00", "end_time": "2022-09-20T09:26:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:26:00+07:00", "end_time": "2022-09-20T09:28:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:28:00+07:00", "end_time": "2022-09-20T09:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:32:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:32:00+07:00", "end_time": "2022-09-20T09:34:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:34:00+07:00", "end_time": "2022-09-20T09:36:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:36:00+07:00", "end_time": "2022-09-20T09:38:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:38:00+07:00", "end_time": "2022-09-20T09:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:42:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:42:00+07:00", "end_time": "2022-09-20T09:44:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:44:00+07:00", "end_time": "2022-09-20T09:46:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:46:00+07:00", "end_time": "2022-09-20T09:48:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:48:00+07:00", "end_time": "2022-09-20T09:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:52:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:52:00+07:00", "end_time": "2022-09-20T09:54:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:54:00+07:00", "end_time": "2022-09-20T09:56:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:56:00+07:00", "end_time": "2022-09-20T09:58:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:58:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "avg": 100}]})

    def test_retrieve_1_hour_without_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_without_result(self,"60MIN")

        self.assertEqual(response.data,{"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "60MIN", "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body": None, "success_rate": [{"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:02:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:02:00+07:00", "end_time": "2022-09-20T09:04:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:04:00+07:00", "end_time": "2022-09-20T09:06:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:06:00+07:00", "end_time": "2022-09-20T09:08:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:08:00+07:00", "end_time": "2022-09-20T09:10:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:12:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:12:00+07:00", "end_time": "2022-09-20T09:14:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:14:00+07:00", "end_time": "2022-09-20T09:16:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:16:00+07:00", "end_time": "2022-09-20T09:18:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:18:00+07:00", "end_time": "2022-09-20T09:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:22:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:22:00+07:00", "end_time": "2022-09-20T09:24:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:24:00+07:00", "end_time": "2022-09-20T09:26:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:26:00+07:00", "end_time": "2022-09-20T09:28:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:28:00+07:00", "end_time": "2022-09-20T09:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:32:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:32:00+07:00", "end_time": "2022-09-20T09:34:00+07:00", "success": 0, "failed": 0}, 
{"start_time": "2022-09-20T09:34:00+07:00", "end_time": "2022-09-20T09:36:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:36:00+07:00", "end_time": "2022-09-20T09:38:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:38:00+07:00", "end_time": "2022-09-20T09:40:00+07:00", "success": 0, "failed": 0}, {"start_time": 
"2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:42:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:42:00+07:00", "end_time": "2022-09-20T09:44:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:44:00+07:00", "end_time": "2022-09-20T09:46:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:46:00+07:00", "end_time": "2022-09-20T09:48:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:48:00+07:00", "end_time": "2022-09-20T09:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:52:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:52:00+07:00", "end_time": "2022-09-20T09:54:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:54:00+07:00", "end_time": "2022-09-20T09:56:00+07:00", "success": 0, "failed": 
0}, {"start_time": "2022-09-20T09:56:00+07:00", "end_time": "2022-09-20T09:58:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:58:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "success": 0, "failed": 0}], "response_time": [{"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:02:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:02:00+07:00", "end_time": "2022-09-20T09:04:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:04:00+07:00", "end_time": "2022-09-20T09:06:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:06:00+07:00", "end_time": "2022-09-20T09:08:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:08:00+07:00", "end_time": "2022-09-20T09:10:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:12:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:12:00+07:00", "end_time": "2022-09-20T09:14:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:14:00+07:00", "end_time": "2022-09-20T09:16:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:16:00+07:00", "end_time": "2022-09-20T09:18:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:18:00+07:00", "end_time": "2022-09-20T09:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:22:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:22:00+07:00", "end_time": "2022-09-20T09:24:00+07:00", "avg": 0}, {"start_time": 
"2022-09-20T09:24:00+07:00", "end_time": "2022-09-20T09:26:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:26:00+07:00", "end_time": "2022-09-20T09:28:00+07:00", "avg": 0}, 
{"start_time": "2022-09-20T09:28:00+07:00", "end_time": "2022-09-20T09:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:32:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:32:00+07:00", "end_time": "2022-09-20T09:34:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:34:00+07:00", "end_time": "2022-09-20T09:36:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:36:00+07:00", "end_time": "2022-09-20T09:38:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:38:00+07:00", "end_time": "2022-09-20T09:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:42:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:42:00+07:00", "end_time": "2022-09-20T09:44:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:44:00+07:00", "end_time": "2022-09-20T09:46:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:46:00+07:00", "end_time": "2022-09-20T09:48:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:48:00+07:00", "end_time": "2022-09-20T09:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:52:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:52:00+07:00", "end_time": "2022-09-20T09:54:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:54:00+07:00", "end_time": "2022-09-20T09:56:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:56:00+07:00", "end_time": "2022-09-20T09:58:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:58:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "avg": 0}]})
    
    
    def test_retrieve_3_hours_with_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_with_result(self,"180MIN")

        self.assertEqual(response.data,{"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "180MIN", "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body": None, "success_rate": [{"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:05:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:05:00+07:00", "end_time": "2022-09-20T07:10:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:10:00+07:00", "end_time": "2022-09-20T07:15:00+07:00", "success": 
0, "failed": 0}, {"start_time": "2022-09-20T07:15:00+07:00", "end_time": "2022-09-20T07:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:25:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:25:00+07:00", "end_time": "2022-09-20T07:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T07:35:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:35:00+07:00", "end_time": "2022-09-20T07:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T07:45:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:45:00+07:00", "end_time": "2022-09-20T07:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:50:00+07:00", "end_time": "2022-09-20T07:55:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:55:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:05:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:05:00+07:00", "end_time": "2022-09-20T08:10:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:10:00+07:00", "end_time": "2022-09-20T08:15:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:15:00+07:00", "end_time": "2022-09-20T08:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:25:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:25:00+07:00", "end_time": "2022-09-20T08:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T08:35:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:35:00+07:00", "end_time": "2022-09-20T08:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T08:45:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:45:00+07:00", "end_time": "2022-09-20T08:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:50:00+07:00", "end_time": "2022-09-20T08:55:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:55:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:05:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:05:00+07:00", "end_time": "2022-09-20T09:10:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:15:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:15:00+07:00", "end_time": "2022-09-20T09:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:25:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:25:00+07:00", "end_time": "2022-09-20T09:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:35:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:35:00+07:00", "end_time": "2022-09-20T09:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:45:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:45:00+07:00", "end_time": "2022-09-20T09:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:55:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:55:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "success": 1, "failed": 0}], "response_time": [{"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:05:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:05:00+07:00", "end_time": "2022-09-20T07:10:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:10:00+07:00", "end_time": "2022-09-20T07:15:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:15:00+07:00", "end_time": "2022-09-20T07:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:25:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:25:00+07:00", "end_time": "2022-09-20T07:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T07:35:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:35:00+07:00", "end_time": "2022-09-20T07:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T07:45:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:45:00+07:00", "end_time": "2022-09-20T07:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:50:00+07:00", "end_time": "2022-09-20T07:55:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:55:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:05:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:05:00+07:00", "end_time": "2022-09-20T08:10:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:10:00+07:00", "end_time": "2022-09-20T08:15:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:15:00+07:00", "end_time": "2022-09-20T08:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:25:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:25:00+07:00", "end_time": "2022-09-20T08:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T08:35:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:35:00+07:00", "end_time": "2022-09-20T08:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T08:45:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:45:00+07:00", "end_time": "2022-09-20T08:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:50:00+07:00", "end_time": "2022-09-20T08:55:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:55:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:05:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:05:00+07:00", "end_time": "2022-09-20T09:10:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:15:00+07:00", "avg": 0}, {"start_time": 
"2022-09-20T09:15:00+07:00", "end_time": "2022-09-20T09:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:25:00+07:00", "avg": 0}, 
{"start_time": "2022-09-20T09:25:00+07:00", "end_time": "2022-09-20T09:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:35:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:35:00+07:00", "end_time": "2022-09-20T09:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:45:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:45:00+07:00", "end_time": "2022-09-20T09:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:55:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:55:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "avg": 100}]})

    def test_retrieve_3_hours_without_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_without_result(self,"180MIN")

        self.assertEqual(response.data,{"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "180MIN", "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body": None, "success_rate": [{"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:05:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:05:00+07:00", "end_time": "2022-09-20T07:10:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:10:00+07:00", "end_time": "2022-09-20T07:15:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:15:00+07:00", "end_time": "2022-09-20T07:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:25:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:25:00+07:00", "end_time": "2022-09-20T07:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T07:35:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:35:00+07:00", "end_time": "2022-09-20T07:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T07:45:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:45:00+07:00", "end_time": "2022-09-20T07:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:50:00+07:00", "end_time": "2022-09-20T07:55:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:55:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:05:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:05:00+07:00", "end_time": "2022-09-20T08:10:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:10:00+07:00", "end_time": "2022-09-20T08:15:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:15:00+07:00", "end_time": "2022-09-20T08:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:25:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:25:00+07:00", "end_time": "2022-09-20T08:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T08:35:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:35:00+07:00", "end_time": "2022-09-20T08:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T08:45:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:45:00+07:00", "end_time": "2022-09-20T08:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:50:00+07:00", "end_time": "2022-09-20T08:55:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:55:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:05:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:05:00+07:00", "end_time": "2022-09-20T09:10:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:15:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:15:00+07:00", "end_time": "2022-09-20T09:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:25:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:25:00+07:00", "end_time": "2022-09-20T09:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:35:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:35:00+07:00", "end_time": "2022-09-20T09:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:45:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:45:00+07:00", "end_time": "2022-09-20T09:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:55:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:55:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "success": 0, "failed": 0}], "response_time": [{"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:05:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:05:00+07:00", "end_time": "2022-09-20T07:10:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:10:00+07:00", "end_time": "2022-09-20T07:15:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:15:00+07:00", "end_time": "2022-09-20T07:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:25:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:25:00+07:00", "end_time": "2022-09-20T07:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T07:35:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:35:00+07:00", "end_time": "2022-09-20T07:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T07:45:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:45:00+07:00", "end_time": "2022-09-20T07:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:50:00+07:00", "end_time": "2022-09-20T07:55:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:55:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:05:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:05:00+07:00", "end_time": "2022-09-20T08:10:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:10:00+07:00", "end_time": "2022-09-20T08:15:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:15:00+07:00", "end_time": "2022-09-20T08:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:25:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:25:00+07:00", "end_time": "2022-09-20T08:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T08:35:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:35:00+07:00", "end_time": "2022-09-20T08:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T08:45:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:45:00+07:00", "end_time": "2022-09-20T08:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:50:00+07:00", "end_time": "2022-09-20T08:55:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:55:00+07:00", 
"end_time": "2022-09-20T09:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:05:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:05:00+07:00", "end_time": "2022-09-20T09:10:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:15:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:15:00+07:00", "end_time": "2022-09-20T09:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:25:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:25:00+07:00", "end_time": "2022-09-20T09:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:35:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:35:00+07:00", "end_time": "2022-09-20T09:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:45:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:45:00+07:00", "end_time": "2022-09-20T09:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:55:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:55:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "avg": 0}]})
    
    
    def test_retrieve_6_hours_with_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_with_result(self,"360MIN")
       
        self.assertEqual(response.data,{"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "360MIN", "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body": None, "success_rate": [{"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:10:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:10:00+07:00", "end_time": "2022-09-20T04:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:20:00+07:00", "end_time": "2022-09-20T04:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:30:00+07:00", "end_time": "2022-09-20T04:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:40:00+07:00", "end_time": "2022-09-20T04:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:50:00+07:00", "end_time": "2022-09-20T05:00:00+07:00", "success": 0, "failed": 
0}, {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:10:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:10:00+07:00", "end_time": "2022-09-20T05:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:20:00+07:00", "end_time": "2022-09-20T05:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:30:00+07:00", "end_time": "2022-09-20T05:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:40:00+07:00", "end_time": "2022-09-20T05:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:50:00+07:00", "end_time": "2022-09-20T06:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:10:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:10:00+07:00", "end_time": "2022-09-20T06:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:20:00+07:00", "end_time": "2022-09-20T06:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:30:00+07:00", "end_time": "2022-09-20T06:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:40:00+07:00", "end_time": "2022-09-20T06:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:50:00+07:00", "end_time": "2022-09-20T07:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:00:00+07:00", "end_time": 
"2022-09-20T07:10:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:10:00+07:00", "end_time": "2022-09-20T07:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T07:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T07:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:50:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:10:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:10:00+07:00", "end_time": "2022-09-20T08:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T08:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T08:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:50:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:10:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "success": 1, "failed": 0}], "response_time": [{"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:10:00+07:00", "avg": 0}, {"start_time": "2022-09-20T04:10:00+07:00", "end_time": "2022-09-20T04:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T04:20:00+07:00", "end_time": "2022-09-20T04:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T04:30:00+07:00", "end_time": "2022-09-20T04:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T04:40:00+07:00", "end_time": "2022-09-20T04:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T04:50:00+07:00", "end_time": "2022-09-20T05:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:10:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:10:00+07:00", "end_time": "2022-09-20T05:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:20:00+07:00", "end_time": "2022-09-20T05:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:30:00+07:00", "end_time": "2022-09-20T05:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:40:00+07:00", "end_time": "2022-09-20T05:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:50:00+07:00", "end_time": "2022-09-20T06:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:10:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:10:00+07:00", "end_time": "2022-09-20T06:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:20:00+07:00", "end_time": "2022-09-20T06:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:30:00+07:00", "end_time": "2022-09-20T06:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:40:00+07:00", "end_time": "2022-09-20T06:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:50:00+07:00", "end_time": "2022-09-20T07:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:10:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:10:00+07:00", "end_time": "2022-09-20T07:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T07:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T07:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:50:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:10:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:10:00+07:00", "end_time": "2022-09-20T08:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T08:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T08:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:50:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:10:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "avg": 100}]})

    def test_retrieve_6_hours_without_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_without_result(self,"360MIN")

        self.assertEqual(response.data,{"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "360MIN", "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], 
"raw_body": None, "success_rate": [{"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:10:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:10:00+07:00", "end_time": "2022-09-20T04:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:20:00+07:00", "end_time": "2022-09-20T04:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:30:00+07:00", "end_time": "2022-09-20T04:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:40:00+07:00", 
"end_time": "2022-09-20T04:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:50:00+07:00", "end_time": "2022-09-20T05:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:10:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:10:00+07:00", "end_time": "2022-09-20T05:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:20:00+07:00", "end_time": "2022-09-20T05:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:30:00+07:00", "end_time": "2022-09-20T05:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:40:00+07:00", "end_time": "2022-09-20T05:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:50:00+07:00", "end_time": "2022-09-20T06:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:10:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:10:00+07:00", "end_time": "2022-09-20T06:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:20:00+07:00", "end_time": "2022-09-20T06:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:30:00+07:00", "end_time": "2022-09-20T06:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:40:00+07:00", "end_time": "2022-09-20T06:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:50:00+07:00", "end_time": "2022-09-20T07:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:10:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:10:00+07:00", "end_time": "2022-09-20T07:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T07:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T07:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:50:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:10:00+07:00", 
"success": 0, "failed": 0}, {"start_time": "2022-09-20T08:10:00+07:00", "end_time": "2022-09-20T08:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T08:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T08:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:50:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:10:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:50:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "success": 0, "failed": 0}], "response_time": [{"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:10:00+07:00", "avg": 0}, {"start_time": "2022-09-20T04:10:00+07:00", "end_time": "2022-09-20T04:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T04:20:00+07:00", "end_time": "2022-09-20T04:30:00+07:00", "avg": 0}, {"start_time": 
"2022-09-20T04:30:00+07:00", "end_time": "2022-09-20T04:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T04:40:00+07:00", "end_time": "2022-09-20T04:50:00+07:00", "avg": 0}, 
{"start_time": "2022-09-20T04:50:00+07:00", "end_time": "2022-09-20T05:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:10:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:10:00+07:00", "end_time": "2022-09-20T05:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:20:00+07:00", "end_time": "2022-09-20T05:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:30:00+07:00", "end_time": "2022-09-20T05:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:40:00+07:00", "end_time": "2022-09-20T05:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:50:00+07:00", "end_time": "2022-09-20T06:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:10:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:10:00+07:00", "end_time": "2022-09-20T06:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:20:00+07:00", "end_time": "2022-09-20T06:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:30:00+07:00", "end_time": "2022-09-20T06:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:40:00+07:00", "end_time": "2022-09-20T06:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:50:00+07:00", "end_time": "2022-09-20T07:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:10:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:10:00+07:00", "end_time": "2022-09-20T07:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T07:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T07:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:50:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:10:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:10:00+07:00", "end_time": "2022-09-20T08:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T08:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T08:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:50:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:10:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:50:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "avg": 0}]})
    
    
    def test_retrieve_12_hours_with_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_with_result(self,"720MIN")

        self.assertEqual(response.data,{"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "720MIN", "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body": None, "success_rate": [{"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T22:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T22:20:00+07:00", "end_time": "2022-09-19T22:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T22:40:00+07:00", "end_time": "2022-09-19T23:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-19T23:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T23:20:00+07:00", "end_time": "2022-09-19T23:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T23:40:00+07:00", "end_time": "2022-09-20T00:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T00:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T00:20:00+07:00", "end_time": "2022-09-20T00:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T00:40:00+07:00", "end_time": "2022-09-20T01:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T01:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T01:20:00+07:00", "end_time": "2022-09-20T01:40:00+07:00", 
"success": 0, "failed": 0}, {"start_time": "2022-09-20T01:40:00+07:00", "end_time": "2022-09-20T02:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T02:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T02:20:00+07:00", "end_time": "2022-09-20T02:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T02:40:00+07:00", "end_time": "2022-09-20T03:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T03:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T03:20:00+07:00", "end_time": "2022-09-20T03:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T03:40:00+07:00", "end_time": "2022-09-20T04:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:20:00+07:00", "end_time": "2022-09-20T04:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:40:00+07:00", "end_time": "2022-09-20T05:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:20:00+07:00", "end_time": "2022-09-20T05:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:40:00+07:00", "end_time": "2022-09-20T06:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:20:00+07:00", "success": 
0, "failed": 0}, {"start_time": "2022-09-20T06:20:00+07:00", "end_time": "2022-09-20T06:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:40:00+07:00", "end_time": "2022-09-20T07:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "success": 1, "failed": 0}], "response_time": [{"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T22:20:00+07:00", "avg": 0}, {"start_time": "2022-09-19T22:20:00+07:00", "end_time": "2022-09-19T22:40:00+07:00", "avg": 0}, {"start_time": "2022-09-19T22:40:00+07:00", "end_time": "2022-09-19T23:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-19T23:20:00+07:00", "avg": 0}, {"start_time": "2022-09-19T23:20:00+07:00", "end_time": "2022-09-19T23:40:00+07:00", "avg": 0}, {"start_time": "2022-09-19T23:40:00+07:00", "end_time": "2022-09-20T00:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T00:20:00+07:00", "avg": 
0}, {"start_time": "2022-09-20T00:20:00+07:00", "end_time": "2022-09-20T00:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T00:40:00+07:00", "end_time": "2022-09-20T01:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T01:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T01:20:00+07:00", "end_time": "2022-09-20T01:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T01:40:00+07:00", "end_time": "2022-09-20T02:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T02:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T02:20:00+07:00", "end_time": "2022-09-20T02:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T02:40:00+07:00", "end_time": "2022-09-20T03:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T03:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T03:20:00+07:00", "end_time": "2022-09-20T03:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T03:40:00+07:00", "end_time": "2022-09-20T04:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T04:20:00+07:00", "end_time": "2022-09-20T04:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T04:40:00+07:00", "end_time": "2022-09-20T05:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:20:00+07:00", "end_time": "2022-09-20T05:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:40:00+07:00", "end_time": "2022-09-20T06:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:20:00+07:00", "end_time": "2022-09-20T06:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:40:00+07:00", "end_time": "2022-09-20T07:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "avg": 100}]})

    def test_retrieve_12_hours_without_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_without_result(self,"720MIN")

        self.assertEqual(response.data,{"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "720MIN", "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body": None, "success_rate": [{"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T22:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T22:20:00+07:00", "end_time": "2022-09-19T22:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T22:40:00+07:00", "end_time": "2022-09-19T23:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-19T23:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T23:20:00+07:00", "end_time": "2022-09-19T23:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T23:40:00+07:00", "end_time": "2022-09-20T00:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T00:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T00:20:00+07:00", "end_time": "2022-09-20T00:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T00:40:00+07:00", "end_time": "2022-09-20T01:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T01:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T01:20:00+07:00", "end_time": "2022-09-20T01:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T01:40:00+07:00", "end_time": "2022-09-20T02:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T02:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T02:20:00+07:00", "end_time": "2022-09-20T02:40:00+07:00", "success": 0, 
"failed": 0}, {"start_time": "2022-09-20T02:40:00+07:00", "end_time": "2022-09-20T03:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T03:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T03:20:00+07:00", "end_time": "2022-09-20T03:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T03:40:00+07:00", "end_time": "2022-09-20T04:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:20:00+07:00", "end_time": "2022-09-20T04:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:40:00+07:00", "end_time": "2022-09-20T05:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:20:00+07:00", "end_time": "2022-09-20T05:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:40:00+07:00", "end_time": "2022-09-20T06:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:20:00+07:00", "end_time": "2022-09-20T06:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:40:00+07:00", "end_time": "2022-09-20T07:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:20:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:40:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "success": 0, "failed": 0}], "response_time": [{"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T22:20:00+07:00", "avg": 0}, {"start_time": "2022-09-19T22:20:00+07:00", "end_time": "2022-09-19T22:40:00+07:00", "avg": 0}, {"start_time": "2022-09-19T22:40:00+07:00", "end_time": "2022-09-19T23:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-19T23:20:00+07:00", "avg": 0}, {"start_time": "2022-09-19T23:20:00+07:00", "end_time": "2022-09-19T23:40:00+07:00", "avg": 0}, {"start_time": "2022-09-19T23:40:00+07:00", "end_time": "2022-09-20T00:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T00:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T00:20:00+07:00", "end_time": "2022-09-20T00:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T00:40:00+07:00", "end_time": "2022-09-20T01:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T01:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T01:20:00+07:00", "end_time": "2022-09-20T01:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T01:40:00+07:00", "end_time": "2022-09-20T02:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T02:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T02:20:00+07:00", "end_time": "2022-09-20T02:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T02:40:00+07:00", "end_time": "2022-09-20T03:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T03:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T03:20:00+07:00", "end_time": "2022-09-20T03:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T03:40:00+07:00", "end_time": "2022-09-20T04:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T04:20:00+07:00", "end_time": "2022-09-20T04:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T04:40:00+07:00", "end_time": "2022-09-20T05:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:20:00+07:00", "end_time": "2022-09-20T05:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:40:00+07:00", "end_time": "2022-09-20T06:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:20:00+07:00", "end_time": "2022-09-20T06:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:40:00+07:00", "end_time": "2022-09-20T07:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:20:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:40:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "avg": 0}]})
    
    
    def test_retrieve_24_hours_with_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_with_result(self,"1440MIN")
        
        self.assertEqual(response.data,{"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "1440MIN", "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body": None, "success_rate": [{"start_time": "2022-09-19T10:00:00+07:00", "end_time": "2022-09-19T10:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T10:30:00+07:00", "end_time": "2022-09-19T11:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T11:00:00+07:00", "end_time": "2022-09-19T11:30:00+07:00", "success": 0, 
"failed": 0}, {"start_time": "2022-09-19T11:30:00+07:00", "end_time": "2022-09-19T12:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T12:00:00+07:00", "end_time": "2022-09-19T12:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T12:30:00+07:00", "end_time": "2022-09-19T13:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T13:00:00+07:00", "end_time": "2022-09-19T13:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T13:30:00+07:00", "end_time": "2022-09-19T14:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T14:00:00+07:00", "end_time": "2022-09-19T14:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T14:30:00+07:00", "end_time": "2022-09-19T15:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T15:00:00+07:00", "end_time": "2022-09-19T15:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T15:30:00+07:00", "end_time": "2022-09-19T16:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T16:00:00+07:00", "end_time": "2022-09-19T16:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T16:30:00+07:00", "end_time": "2022-09-19T17:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T17:00:00+07:00", "end_time": "2022-09-19T17:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T17:30:00+07:00", "end_time": "2022-09-19T18:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T18:00:00+07:00", "end_time": "2022-09-19T18:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T18:30:00+07:00", "end_time": "2022-09-19T19:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T19:00:00+07:00", "end_time": "2022-09-19T19:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T19:30:00+07:00", "end_time": "2022-09-19T20:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T20:00:00+07:00", "end_time": "2022-09-19T20:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T20:30:00+07:00", "end_time": "2022-09-19T21:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T21:00:00+07:00", "end_time": "2022-09-19T21:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T21:30:00+07:00", "end_time": "2022-09-19T22:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T22:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T22:30:00+07:00", "end_time": "2022-09-19T23:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-19T23:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T23:30:00+07:00", "end_time": "2022-09-20T00:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T00:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T00:30:00+07:00", "end_time": "2022-09-20T01:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T01:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T01:30:00+07:00", "end_time": "2022-09-20T02:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T02:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T02:30:00+07:00", "end_time": "2022-09-20T03:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T03:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T03:30:00+07:00", "end_time": "2022-09-20T04:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:30:00+07:00", "end_time": "2022-09-20T05:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:30:00+07:00", "end_time": "2022-09-20T06:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:30:00+07:00", "end_time": "2022-09-20T07:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "success": 1, "failed": 0}], "response_time": [{"start_time": 
"2022-09-19T10:00:00+07:00", "end_time": "2022-09-19T10:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T10:30:00+07:00", "end_time": "2022-09-19T11:00:00+07:00", "avg": 0}, 
{"start_time": "2022-09-19T11:00:00+07:00", "end_time": "2022-09-19T11:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T11:30:00+07:00", "end_time": "2022-09-19T12:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T12:00:00+07:00", "end_time": "2022-09-19T12:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T12:30:00+07:00", "end_time": "2022-09-19T13:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T13:00:00+07:00", "end_time": "2022-09-19T13:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T13:30:00+07:00", "end_time": "2022-09-19T14:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T14:00:00+07:00", "end_time": "2022-09-19T14:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T14:30:00+07:00", "end_time": "2022-09-19T15:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T15:00:00+07:00", "end_time": "2022-09-19T15:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T15:30:00+07:00", "end_time": "2022-09-19T16:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T16:00:00+07:00", "end_time": "2022-09-19T16:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T16:30:00+07:00", "end_time": "2022-09-19T17:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T17:00:00+07:00", "end_time": "2022-09-19T17:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T17:30:00+07:00", "end_time": "2022-09-19T18:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T18:00:00+07:00", "end_time": "2022-09-19T18:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T18:30:00+07:00", "end_time": "2022-09-19T19:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T19:00:00+07:00", "end_time": "2022-09-19T19:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T19:30:00+07:00", "end_time": "2022-09-19T20:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T20:00:00+07:00", "end_time": "2022-09-19T20:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T20:30:00+07:00", "end_time": "2022-09-19T21:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T21:00:00+07:00", "end_time": "2022-09-19T21:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T21:30:00+07:00", "end_time": "2022-09-19T22:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T22:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T22:30:00+07:00", "end_time": "2022-09-19T23:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-19T23:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T23:30:00+07:00", "end_time": "2022-09-20T00:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T00:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T00:30:00+07:00", "end_time": "2022-09-20T01:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T01:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T01:30:00+07:00", "end_time": "2022-09-20T02:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T02:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T02:30:00+07:00", "end_time": "2022-09-20T03:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T03:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T03:30:00+07:00", "end_time": "2022-09-20T04:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T04:30:00+07:00", "end_time": "2022-09-20T05:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:30:00+07:00", "end_time": "2022-09-20T06:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:30:00+07:00", "end_time": "2022-09-20T07:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "avg": 100}]})

    def test_retrieve_24_hours_without_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_without_result(self,"1440MIN")
        
        self.assertEqual(response.data,{"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "1440MIN", "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body": None, "success_rate": [{"start_time": "2022-09-19T10:00:00+07:00", "end_time": "2022-09-19T10:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T10:30:00+07:00", "end_time": "2022-09-19T11:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T11:00:00+07:00", "end_time": "2022-09-19T11:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T11:30:00+07:00", "end_time": "2022-09-19T12:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T12:00:00+07:00", "end_time": "2022-09-19T12:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T12:30:00+07:00", "end_time": "2022-09-19T13:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T13:00:00+07:00", "end_time": "2022-09-19T13:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T13:30:00+07:00", "end_time": "2022-09-19T14:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T14:00:00+07:00", "end_time": "2022-09-19T14:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T14:30:00+07:00", "end_time": "2022-09-19T15:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T15:00:00+07:00", "end_time": "2022-09-19T15:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T15:30:00+07:00", "end_time": "2022-09-19T16:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T16:00:00+07:00", "end_time": "2022-09-19T16:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T16:30:00+07:00", "end_time": "2022-09-19T17:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T17:00:00+07:00", "end_time": "2022-09-19T17:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T17:30:00+07:00", "end_time": "2022-09-19T18:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T18:00:00+07:00", "end_time": "2022-09-19T18:30:00+07:00", "success": 0, "failed": 0}, 
{"start_time": "2022-09-19T18:30:00+07:00", "end_time": "2022-09-19T19:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T19:00:00+07:00", "end_time": "2022-09-19T19:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T19:30:00+07:00", "end_time": "2022-09-19T20:00:00+07:00", "success": 0, "failed": 0}, {"start_time": 
"2022-09-19T20:00:00+07:00", "end_time": "2022-09-19T20:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T20:30:00+07:00", "end_time": "2022-09-19T21:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T21:00:00+07:00", "end_time": "2022-09-19T21:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T21:30:00+07:00", "end_time": "2022-09-19T22:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T22:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T22:30:00+07:00", "end_time": "2022-09-19T23:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-19T23:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T23:30:00+07:00", "end_time": "2022-09-20T00:00:00+07:00", "success": 0, "failed": 
0}, {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T00:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T00:30:00+07:00", "end_time": "2022-09-20T01:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T01:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T01:30:00+07:00", "end_time": "2022-09-20T02:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T02:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T02:30:00+07:00", "end_time": "2022-09-20T03:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T03:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T03:30:00+07:00", "end_time": "2022-09-20T04:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:30:00+07:00", "end_time": "2022-09-20T05:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:30:00+07:00", "end_time": "2022-09-20T06:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:00:00+07:00", "end_time": 
"2022-09-20T06:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:30:00+07:00", "end_time": "2022-09-20T07:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:30:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "success": 0, "failed": 0}], "response_time": [{"start_time": "2022-09-19T10:00:00+07:00", "end_time": "2022-09-19T10:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T10:30:00+07:00", "end_time": "2022-09-19T11:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T11:00:00+07:00", "end_time": "2022-09-19T11:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T11:30:00+07:00", "end_time": "2022-09-19T12:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T12:00:00+07:00", "end_time": "2022-09-19T12:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T12:30:00+07:00", "end_time": "2022-09-19T13:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T13:00:00+07:00", "end_time": "2022-09-19T13:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T13:30:00+07:00", "end_time": "2022-09-19T14:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T14:00:00+07:00", "end_time": "2022-09-19T14:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T14:30:00+07:00", "end_time": "2022-09-19T15:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T15:00:00+07:00", "end_time": "2022-09-19T15:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T15:30:00+07:00", "end_time": "2022-09-19T16:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T16:00:00+07:00", "end_time": "2022-09-19T16:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T16:30:00+07:00", "end_time": "2022-09-19T17:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T17:00:00+07:00", "end_time": "2022-09-19T17:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T17:30:00+07:00", "end_time": "2022-09-19T18:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T18:00:00+07:00", "end_time": "2022-09-19T18:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T18:30:00+07:00", "end_time": "2022-09-19T19:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T19:00:00+07:00", "end_time": "2022-09-19T19:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T19:30:00+07:00", "end_time": "2022-09-19T20:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T20:00:00+07:00", "end_time": "2022-09-19T20:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T20:30:00+07:00", "end_time": "2022-09-19T21:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T21:00:00+07:00", "end_time": "2022-09-19T21:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T21:30:00+07:00", "end_time": "2022-09-19T22:00:00+07:00", "avg": 0}, {"start_time": 
"2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T22:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T22:30:00+07:00", "end_time": "2022-09-19T23:00:00+07:00", "avg": 0}, 
{"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-19T23:30:00+07:00", "avg": 0}, {"start_time": "2022-09-19T23:30:00+07:00", "end_time": "2022-09-20T00:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T00:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T00:30:00+07:00", "end_time": "2022-09-20T01:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T01:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T01:30:00+07:00", "end_time": "2022-09-20T02:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T02:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T02:30:00+07:00", "end_time": "2022-09-20T03:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T03:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T03:30:00+07:00", "end_time": "2022-09-20T04:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T04:30:00+07:00", "end_time": "2022-09-20T05:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:30:00+07:00", "end_time": "2022-09-20T06:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:30:00+07:00", "end_time": "2022-09-20T07:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:30:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "avg": 0}]})

class StatsAPIMonitor(APITestCase):
    test_url = reverse('api-monitor-stats')
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    mock_current_time = local_timezone.localize(datetime(2022, 9, 20, 10))

    def setUp(self):
        # Mock time function
        timezone.now = lambda: self.mock_current_time
    
    def test_stats_with_result(self):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        monitor = APIMonitor.objects.create(
            user=user,
            name='Test Monitor',
            method='GET',
            url='Test Path',
            schedule='1440MIN',
            body_type='FORM',
        )
        APIMonitorResult.objects.create(
            monitor=monitor,
            execution_time=self.mock_current_time,
            status_code=200,
            response_time=100,
            success=True,
            log_response='{}'
        )

        response = self.client.get(self.test_url,format="json",**header)
        self.assertEqual(response.data,{"success_rate": [{"start_time": "2022-09-19T10:00:00+07:00", "end_time": "2022-09-19T11:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T11:00:00+07:00", "end_time": "2022-09-19T12:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T12:00:00+07:00", "end_time": "2022-09-19T13:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T13:00:00+07:00", "end_time": "2022-09-19T14:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T14:00:00+07:00", "end_time": "2022-09-19T15:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T15:00:00+07:00", "end_time": "2022-09-19T16:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T16:00:00+07:00", "end_time": "2022-09-19T17:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T17:00:00+07:00", "end_time": "2022-09-19T18:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T18:00:00+07:00", "end_time": "2022-09-19T19:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T19:00:00+07:00", "end_time": "2022-09-19T20:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T20:00:00+07:00", "end_time": "2022-09-19T21:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T21:00:00+07:00", "end_time": "2022-09-19T22:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T23:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-20T00:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T01:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T02:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T03:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T04:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:00:00+07:00", 
"end_time": "2022-09-20T05:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T06:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T07:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "success": 1, "failed": 0}], "response_time": [{"start_time": "2022-09-19T10:00:00+07:00", "end_time": "2022-09-19T11:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T11:00:00+07:00", "end_time": "2022-09-19T12:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T12:00:00+07:00", "end_time": "2022-09-19T13:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T13:00:00+07:00", "end_time": "2022-09-19T14:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T14:00:00+07:00", "end_time": "2022-09-19T15:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T15:00:00+07:00", "end_time": "2022-09-19T16:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T16:00:00+07:00", "end_time": "2022-09-19T17:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T17:00:00+07:00", "end_time": "2022-09-19T18:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T18:00:00+07:00", "end_time": "2022-09-19T19:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T19:00:00+07:00", "end_time": "2022-09-19T20:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T20:00:00+07:00", "end_time": "2022-09-19T21:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T21:00:00+07:00", "end_time": "2022-09-19T22:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T23:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-20T00:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T01:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T02:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T03:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T04:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T05:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T06:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T07:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "avg": 100}]})


    def test_stats_without_result(self):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        monitor = APIMonitor.objects.create(
            user=user,
            name='Test Monitor',
            method='GET',
            url='Test Path',
            schedule='1440MIN',
            body_type='FORM',
        )

        response = self.client.get(self.test_url,format="json",**header)
        self.assertEqual(response.data,{"success_rate": [{"start_time": "2022-09-19T10:00:00+07:00", "end_time": "2022-09-19T11:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T11:00:00+07:00", "end_time": "2022-09-19T12:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T12:00:00+07:00", "end_time": "2022-09-19T13:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T13:00:00+07:00", "end_time": "2022-09-19T14:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T14:00:00+07:00", "end_time": "2022-09-19T15:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T15:00:00+07:00", "end_time": "2022-09-19T16:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T16:00:00+07:00", "end_time": "2022-09-19T17:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T17:00:00+07:00", "end_time": "2022-09-19T18:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T18:00:00+07:00", "end_time": "2022-09-19T19:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T19:00:00+07:00", "end_time": "2022-09-19T20:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T20:00:00+07:00", "end_time": "2022-09-19T21:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T21:00:00+07:00", "end_time": "2022-09-19T22:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T23:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-20T00:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T01:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T02:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T03:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T04:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T05:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T06:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T07:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:00:00+07:00", "end_time": 
"2022-09-20T08:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "success": 0, "failed": 0}], "response_time": [{"start_time": "2022-09-19T10:00:00+07:00", "end_time": "2022-09-19T11:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T11:00:00+07:00", "end_time": "2022-09-19T12:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T12:00:00+07:00", "end_time": "2022-09-19T13:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T13:00:00+07:00", "end_time": "2022-09-19T14:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T14:00:00+07:00", "end_time": "2022-09-19T15:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T15:00:00+07:00", "end_time": "2022-09-19T16:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T16:00:00+07:00", "end_time": "2022-09-19T17:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T17:00:00+07:00", "end_time": "2022-09-19T18:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T18:00:00+07:00", "end_time": "2022-09-19T19:00:00+07:00", 
"avg": 0}, {"start_time": "2022-09-19T19:00:00+07:00", "end_time": "2022-09-19T20:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T20:00:00+07:00", "end_time": "2022-09-19T21:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T21:00:00+07:00", "end_time": "2022-09-19T22:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T23:00:00+07:00", "avg": 0}, {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-20T00:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T01:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T02:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T03:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T04:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T05:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T06:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T07:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "avg": 0}, {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "avg": 0}]})


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
            response_time=100,
            success=True,
            status_code=200,
            log_response='{}'
        )

        APIMonitorResult.objects.create(
            monitor=monitor,
            execution_time=self.mock_current_time,
            response_time=75,
            success=True,
            status_code=200,
            log_response='{}'
        )

        APIMonitorResult.objects.create(
            monitor=monitor,
            execution_time=self.mock_current_time,
            response_time=100,
            success=True,
            status_code=200,
            log_response='{}'
        )

        APIMonitorResult.objects.create(
            monitor=monitor,
            execution_time=self.mock_current_time,
            response_time=50,
            success=False,
            status_code=200,
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
                    "execution_time": "2022-09-20T10:00:00+07:00",
                    "id": 4,
                    "log_error": "",
                    "log_response": "{}",
                    "monitor": 1,
                    "response_time": 50,
                    "status_code": 200,
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
                "raw_body": {
                    "body": "Test Body",
                    "id": 1,
                    "monitor": 1
                },
                "schedule": "10MIN",
                "success_rate": "75.0",
                "success_rate_history": [
                    {
                        "end_time": "2022-09-19T11:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T10:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T12:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T11:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T13:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T12:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T14:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T13:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T15:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T14:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T16:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T15:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T17:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T16:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T18:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T17:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T19:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T18:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T20:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T19:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T21:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T20:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T22:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T21:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T23:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T22:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T00:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T23:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T01:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-20T00:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T02:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-20T01:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T03:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-20T02:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T04:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-20T03:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T05:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-20T04:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T06:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-20T05:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T07:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-20T06:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T08:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-20T07:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T09:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-20T08:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T10:00:00+07:00",
                        "failed": 1,
                        "start_time": "2022-09-20T09:00:00+07:00",
                        "success": 3
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
                "raw_body": {
                    "body": "Test Body",
                    "id": 1,
                    "monitor": 1
                },
                "schedule": "10MIN",
                "success_rate": "100.0",
                "success_rate_history": [
                    {
                        "end_time": "2022-09-19T11:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T10:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T12:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T11:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T13:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T12:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T14:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T13:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T15:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T14:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T16:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T15:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T17:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T16:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T18:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T17:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T19:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T18:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T20:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T19:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T21:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T20:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T22:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T21:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-19T23:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T22:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T00:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-19T23:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T01:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-20T00:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T02:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-20T01:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T03:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-20T02:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T04:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-20T03:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T05:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-20T04:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T06:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-20T05:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T07:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-20T06:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T08:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-20T07:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T09:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-20T08:00:00+07:00",
                        "success": 0
                    },
                    {
                        "end_time": "2022-09-20T10:00:00+07:00",
                        "failed": 0,
                        "start_time": "2022-09-20T09:00:00+07:00",
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
            response_time=100,
            success=True,
            status_code=200,
            log_response='{}'
        )

        APIMonitorResult.objects.create(
            monitor=monitor,
            execution_time=self.mock_current_time,
            response_time=75,
            status_code=200,
            success=True,
            log_response='{}'
        )

        APIMonitorResult.objects.create(
            monitor=monitor,
            execution_time=self.mock_current_time,
            response_time=100,
            success=True,
            status_code=200,
            log_response='{}'
        )

        APIMonitorResult.objects.create(
            monitor=monitor,
            execution_time=self.mock_current_time,
            response_time=50,
            status_code=200,
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
            response_time=100,
            status_code=200,
            success=True,
            log_response='{}'
        )

        APIMonitorResult.objects.create(
            monitor=monitor,
            execution_time=self.mock_current_time,
            response_time=75,
            status_code=200,
            success=True,
            log_response='{}'
        )

        APIMonitorResult.objects.create(
            monitor=monitor,
            execution_time=self.mock_current_time,
            response_time=100,
            status_code=200,
            success=True,
            log_response='{}'
        )

        APIMonitorResult.objects.create(
            monitor=monitor,
            execution_time=self.mock_current_time,
            response_time=50,
            status_code=500,
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

    # PBI-15-edit-api-monitor-backend
    def test_user_can_edit_api_monitor_simple(self):
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

        # 1. Create Object
        create_new_monitor_test_path = reverse('api-monitor-list')
        self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)

        # 2. Update Object
        monitor_value = {
            'name': 'UPDATED Test Monitor',
            'method': 'POST',
            'url': 'Test Path',
            'schedule': '30MIN',
            'body_type': 'RAW',
        }
        queryparam_value = [
            {
                'key': 'ONLY key',
                'value': 'ONLY value',
            }
        ]
        monitorheader_value = [
            {
                'key': 'key3',
                'value': 'value3'
            },
            {
                'key': 'NEW FROM UPDATE key',
                'value': 'NEW FROM UPDATE value'
            }
        ]
        monitorbodyform_value = "This doesn't matter since body type is FORM"
        monitorrawbody_value = "Valid raw body"

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

        target_monitor_id = APIMonitor.objects.filter(user=user)[:1].get().id
        edit_monitor_path = reverse('api-monitor-detail', kwargs={'pk': target_monitor_id})
        response = self.client.put(edit_monitor_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'UPDATED Test Monitor')
        self.assertEqual(response.data['method'], 'POST')
        self.assertEqual(response.data['url'], 'Test Path')
        self.assertEqual(response.data['schedule'], '30MIN')
        self.assertEqual(response.data['body_type'], 'RAW')
        self.assertEqual(len(response.data['query_params']), 1)
        self.assertEqual(len(response.data['headers']), 2)
        self.assertEqual(len(response.data['body_form']), 0)
        self.assertEqual(response.data['raw_body']['body'], "Valid raw body")
