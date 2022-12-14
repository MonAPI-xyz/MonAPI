from unittest import TestCase
import pytz
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django_test_migrations.contrib.unittest_case import MigratorTestCase


from apimonitor.models import APIMonitor, APIMonitorBodyForm, APIMonitorHeader, APIMonitorQueryParam, APIMonitorRawBody, \
    APIMonitorResult, AssertionExcludeKey
from login.models import Team, TeamMember, MonAPIToken
from statuspage.models import StatusPageCategory


class DetailListAPIMonitor(APITestCase):
    test_url = reverse('api-monitor-detail', args=[1])
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    mock_current_time = local_timezone.localize(datetime(2022, 9, 20, 10))

    def setUp(self):
        # Mock time function
        timezone.now = lambda: self.mock_current_time

    def init_for_test_retrieve_without_result(self, range_schedule):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        monitor = APIMonitor.objects.create(
            team=team,
            name='Test Monitor',
            method='GET',
            url='Test Path',
            schedule=range_schedule,
            body_type='FORM',
        )

        response = self.client.get(self.test_url, {"range": range_schedule}, format="json", **header)
        return response

    def init_for_test_retrieve_with_result(self, range_schedule):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        monitor = APIMonitor.objects.create(
            team=team,
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

        response = self.client.get(self.test_url, {"range": range_schedule}, format="json", **header)
        return response

    def test_retrieve_30_min_with_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_with_result(self, "30MIN")

        self.assertEqual(response.data,
                         {"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "30MIN",
                          "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body":
                              None, 'previous_step_id': None, 'status_page_category': None, 'status_page_category_id': None, "success_rate": [
                             {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:31:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:31:00+07:00", "end_time": "2022-09-20T09:32:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:32:00+07:00", "end_time": "2022-09-20T09:33:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:33:00+07:00", "end_time": "2022-09-20T09:34:00+07:00",
                              "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:34:00+07:00", "end_time":
                                 "2022-09-20T09:35:00+07:00", "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:35:00+07:00", "end_time": "2022-09-20T09:36:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:36:00+07:00", "end_time": "2022-09-20T09:37:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:37:00+07:00", "end_time": "2022-09-20T09:38:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:38:00+07:00", "end_time": "2022-09-20T09:39:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:39:00+07:00", "end_time": "2022-09-20T09:40:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:41:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:41:00+07:00", "end_time": "2022-09-20T09:42:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:42:00+07:00", "end_time": "2022-09-20T09:43:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:43:00+07:00", "end_time": "2022-09-20T09:44:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:44:00+07:00", "end_time": "2022-09-20T09:45:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:45:00+07:00", "end_time": "2022-09-20T09:46:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:46:00+07:00", "end_time": "2022-09-20T09:47:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:47:00+07:00", "end_time": "2022-09-20T09:48:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:48:00+07:00", "end_time": "2022-09-20T09:49:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:49:00+07:00", "end_time": "2022-09-20T09:50:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:51:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:51:00+07:00", "end_time": "2022-09-20T09:52:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:52:00+07:00", "end_time": "2022-09-20T09:53:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:53:00+07:00", "end_time": "2022-09-20T09:54:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:54:00+07:00", "end_time": "2022-09-20T09:55:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:55:00+07:00", "end_time": "2022-09-20T09:56:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:56:00+07:00", "end_time": "2022-09-20T09:57:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:57:00+07:00", "end_time": "2022-09-20T09:58:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:58:00+07:00", "end_time": "2022-09-20T09:59:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:59:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                              "success": 1, "failed": 0}], "response_time": [
                             {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:31:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:31:00+07:00", "end_time": "2022-09-20T09:32:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:32:00+07:00", "end_time": "2022-09-20T09:33:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:33:00+07:00", "end_time": "2022-09-20T09:34:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:34:00+07:00", "end_time": "2022-09-20T09:35:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:35:00+07:00", "end_time": "2022-09-20T09:36:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:36:00+07:00", "end_time": "2022-09-20T09:37:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:37:00+07:00", "end_time": "2022-09-20T09:38:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:38:00+07:00", "end_time": "2022-09-20T09:39:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:39:00+07:00", "end_time": "2022-09-20T09:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:41:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:41:00+07:00", "end_time": "2022-09-20T09:42:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:42:00+07:00", "end_time": "2022-09-20T09:43:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:43:00+07:00", "end_time": "2022-09-20T09:44:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:44:00+07:00", "end_time": "2022-09-20T09:45:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:45:00+07:00", "end_time": "2022-09-20T09:46:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:46:00+07:00", "end_time": "2022-09-20T09:47:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:47:00+07:00", "end_time": "2022-09-20T09:48:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:48:00+07:00", "end_time": "2022-09-20T09:49:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:49:00+07:00", "end_time": "2022-09-20T09:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:51:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:51:00+07:00", "end_time": "2022-09-20T09:52:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:52:00+07:00", "end_time": "2022-09-20T09:53:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:53:00+07:00", "end_time": "2022-09-20T09:54:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:54:00+07:00", "end_time": "2022-09-20T09:55:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:55:00+07:00", "end_time": "2022-09-20T09:56:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:56:00+07:00", "end_time": "2022-09-20T09:57:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:57:00+07:00", "end_time": "2022-09-20T09:58:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:58:00+07:00", "end_time": "2022-09-20T09:59:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:59:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                              "avg": 100}],
                          'assertion_type': 'DISABLED', 'assertion_value': '', 'is_assert_json_schema_only': False, 'exclude_keys': []
                          })

    def test_retrieve_30_min_without_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_without_result(self,
                                                                              "30MIN")  # print(json.dumps(response.data))

        self.assertEqual(response.data,
                         {"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "30MIN",
                          "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body":
                              None, 'previous_step_id': None, 'status_page_category': None, 'status_page_category_id': None, "success_rate": [
                             {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:31:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:31:00+07:00", "end_time": "2022-09-20T09:32:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:32:00+07:00", "end_time": "2022-09-20T09:33:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:33:00+07:00", "end_time": "2022-09-20T09:34:00+07:00",
                              "success": 0, "failed": 0}, {"start_time": "2022-09-20T09:34:00+07:00", "end_time":
                                 "2022-09-20T09:35:00+07:00", "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:35:00+07:00", "end_time": "2022-09-20T09:36:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:36:00+07:00", "end_time": "2022-09-20T09:37:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:37:00+07:00", "end_time": "2022-09-20T09:38:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:38:00+07:00", "end_time": "2022-09-20T09:39:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:39:00+07:00", "end_time": "2022-09-20T09:40:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:41:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:41:00+07:00", "end_time": "2022-09-20T09:42:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:42:00+07:00", "end_time": "2022-09-20T09:43:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:43:00+07:00", "end_time": "2022-09-20T09:44:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:44:00+07:00", "end_time": "2022-09-20T09:45:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:45:00+07:00", "end_time": "2022-09-20T09:46:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:46:00+07:00", "end_time": "2022-09-20T09:47:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:47:00+07:00", "end_time": "2022-09-20T09:48:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:48:00+07:00", "end_time": "2022-09-20T09:49:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:49:00+07:00", "end_time": "2022-09-20T09:50:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:51:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:51:00+07:00", "end_time": "2022-09-20T09:52:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:52:00+07:00", "end_time": "2022-09-20T09:53:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:53:00+07:00", "end_time": "2022-09-20T09:54:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:54:00+07:00", "end_time": "2022-09-20T09:55:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:55:00+07:00", "end_time": "2022-09-20T09:56:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:56:00+07:00", "end_time": "2022-09-20T09:57:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:57:00+07:00", "end_time": "2022-09-20T09:58:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:58:00+07:00", "end_time": "2022-09-20T09:59:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:59:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                              "success": 0, "failed": 0}], "response_time": [
                             {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:31:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:31:00+07:00", "end_time": "2022-09-20T09:32:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:32:00+07:00", "end_time": "2022-09-20T09:33:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:33:00+07:00", "end_time": "2022-09-20T09:34:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:34:00+07:00", "end_time": "2022-09-20T09:35:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:35:00+07:00", "end_time": "2022-09-20T09:36:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:36:00+07:00", "end_time": "2022-09-20T09:37:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:37:00+07:00", "end_time": "2022-09-20T09:38:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:38:00+07:00", "end_time": "2022-09-20T09:39:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:39:00+07:00", "end_time": "2022-09-20T09:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:41:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:41:00+07:00", "end_time": "2022-09-20T09:42:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:42:00+07:00", "end_time": "2022-09-20T09:43:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:43:00+07:00", "end_time": "2022-09-20T09:44:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:44:00+07:00", "end_time": "2022-09-20T09:45:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:45:00+07:00", "end_time": "2022-09-20T09:46:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:46:00+07:00", "end_time": "2022-09-20T09:47:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:47:00+07:00", "end_time": "2022-09-20T09:48:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:48:00+07:00", "end_time": "2022-09-20T09:49:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:49:00+07:00", "end_time": "2022-09-20T09:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:51:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:51:00+07:00", "end_time": "2022-09-20T09:52:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:52:00+07:00", "end_time": "2022-09-20T09:53:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:53:00+07:00", "end_time": "2022-09-20T09:54:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:54:00+07:00", "end_time": "2022-09-20T09:55:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:55:00+07:00", "end_time": "2022-09-20T09:56:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:56:00+07:00", "end_time": "2022-09-20T09:57:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:57:00+07:00", "end_time": "2022-09-20T09:58:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:58:00+07:00", "end_time": "2022-09-20T09:59:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:59:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                              "avg": 0}],
                          'assertion_type': 'DISABLED', 'assertion_value': '', 'is_assert_json_schema_only': False, 'exclude_keys': []
                          })

    def test_retrieve_1_hour_with_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_with_result(self, "60MIN")

        self.assertEqual(response.data,
                         {"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "60MIN",
                          "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body": None, 'previous_step_id': None,
                          'status_page_category': None, 'status_page_category_id': None, 
                          "success_rate": [
                              {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:02:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:02:00+07:00", "end_time": "2022-09-20T09:04:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:04:00+07:00", "end_time": "2022-09-20T09:06:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:06:00+07:00", "end_time": "2022-09-20T09:08:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:08:00+07:00", "end_time": "2022-09-20T09:10:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:12:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:12:00+07:00", "end_time": "2022-09-20T09:14:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:14:00+07:00", "end_time": "2022-09-20T09:16:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:16:00+07:00", "end_time": "2022-09-20T09:18:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:18:00+07:00", "end_time": "2022-09-20T09:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:22:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:22:00+07:00", "end_time": "2022-09-20T09:24:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:24:00+07:00", "end_time": "2022-09-20T09:26:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:26:00+07:00", "end_time": "2022-09-20T09:28:00+07:00",
                               "success": 0,
                               "failed": 0},
                              {"start_time": "2022-09-20T09:28:00+07:00", "end_time": "2022-09-20T09:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:32:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:32:00+07:00", "end_time": "2022-09-20T09:34:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:34:00+07:00", "end_time": "2022-09-20T09:36:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:36:00+07:00", "end_time": "2022-09-20T09:38:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:38:00+07:00", "end_time": "2022-09-20T09:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:42:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:42:00+07:00", "end_time": "2022-09-20T09:44:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:44:00+07:00", "end_time": "2022-09-20T09:46:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:46:00+07:00", "end_time": "2022-09-20T09:48:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:48:00+07:00", "end_time": "2022-09-20T09:50:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:52:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:52:00+07:00", "end_time": "2022-09-20T09:54:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:54:00+07:00", "end_time": "2022-09-20T09:56:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:56:00+07:00", "end_time": "2022-09-20T09:58:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:58:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                               "success": 1, "failed": 0}], "response_time": [
                             {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:02:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:02:00+07:00", "end_time": "2022-09-20T09:04:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:04:00+07:00", "end_time": "2022-09-20T09:06:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:06:00+07:00", "end_time": "2022-09-20T09:08:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:08:00+07:00", "end_time": "2022-09-20T09:10:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:12:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:12:00+07:00", "end_time": "2022-09-20T09:14:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:14:00+07:00", "end_time": "2022-09-20T09:16:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:16:00+07:00", "end_time": "2022-09-20T09:18:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:18:00+07:00", "end_time": "2022-09-20T09:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:22:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:22:00+07:00", "end_time": "2022-09-20T09:24:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:24:00+07:00", "end_time": "2022-09-20T09:26:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:26:00+07:00", "end_time": "2022-09-20T09:28:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:28:00+07:00", "end_time": "2022-09-20T09:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:32:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:32:00+07:00", "end_time": "2022-09-20T09:34:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:34:00+07:00", "end_time": "2022-09-20T09:36:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:36:00+07:00", "end_time": "2022-09-20T09:38:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:38:00+07:00", "end_time": "2022-09-20T09:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:42:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:42:00+07:00", "end_time": "2022-09-20T09:44:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:44:00+07:00", "end_time": "2022-09-20T09:46:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:46:00+07:00", "end_time": "2022-09-20T09:48:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:48:00+07:00", "end_time": "2022-09-20T09:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:52:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:52:00+07:00", "end_time": "2022-09-20T09:54:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:54:00+07:00", "end_time": "2022-09-20T09:56:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:56:00+07:00", "end_time": "2022-09-20T09:58:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:58:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                              "avg": 100}],
                          'assertion_type': 'DISABLED', 'assertion_value': '', 'is_assert_json_schema_only': False, 'exclude_keys': []
                          })

    def test_retrieve_1_hour_without_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_without_result(self, "60MIN")

        self.assertEqual(response.data,
                         {"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "60MIN",
                          "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body": None, 'previous_step_id': None,
                          'status_page_category': None, 'status_page_category_id': None, 
                          "success_rate": [
                              {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:02:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:02:00+07:00", "end_time": "2022-09-20T09:04:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:04:00+07:00", "end_time": "2022-09-20T09:06:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:06:00+07:00", "end_time": "2022-09-20T09:08:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:08:00+07:00", "end_time": "2022-09-20T09:10:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:12:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:12:00+07:00", "end_time": "2022-09-20T09:14:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:14:00+07:00", "end_time": "2022-09-20T09:16:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:16:00+07:00", "end_time": "2022-09-20T09:18:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:18:00+07:00", "end_time": "2022-09-20T09:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:22:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:22:00+07:00", "end_time": "2022-09-20T09:24:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:24:00+07:00", "end_time": "2022-09-20T09:26:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:26:00+07:00", "end_time": "2022-09-20T09:28:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:28:00+07:00", "end_time": "2022-09-20T09:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:32:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:32:00+07:00", "end_time": "2022-09-20T09:34:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:34:00+07:00", "end_time": "2022-09-20T09:36:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:36:00+07:00", "end_time": "2022-09-20T09:38:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:38:00+07:00", "end_time": "2022-09-20T09:40:00+07:00",
                               "success": 0, "failed": 0}, {"start_time":
                                                                "2022-09-20T09:40:00+07:00",
                                                            "end_time": "2022-09-20T09:42:00+07:00", "success": 0,
                                                            "failed": 0},
                              {"start_time": "2022-09-20T09:42:00+07:00", "end_time": "2022-09-20T09:44:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:44:00+07:00", "end_time": "2022-09-20T09:46:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:46:00+07:00", "end_time": "2022-09-20T09:48:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:48:00+07:00", "end_time": "2022-09-20T09:50:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:52:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:52:00+07:00", "end_time": "2022-09-20T09:54:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:54:00+07:00", "end_time": "2022-09-20T09:56:00+07:00",
                               "success": 0, "failed":
                                   0},
                              {"start_time": "2022-09-20T09:56:00+07:00", "end_time": "2022-09-20T09:58:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:58:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                               "success": 0, "failed": 0}], "response_time": [
                             {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:02:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:02:00+07:00", "end_time": "2022-09-20T09:04:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:04:00+07:00", "end_time": "2022-09-20T09:06:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:06:00+07:00", "end_time": "2022-09-20T09:08:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:08:00+07:00", "end_time": "2022-09-20T09:10:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:12:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:12:00+07:00", "end_time": "2022-09-20T09:14:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:14:00+07:00", "end_time": "2022-09-20T09:16:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:16:00+07:00", "end_time": "2022-09-20T09:18:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:18:00+07:00", "end_time": "2022-09-20T09:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:22:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:22:00+07:00", "end_time": "2022-09-20T09:24:00+07:00",
                              "avg": 0}, {"start_time":
                                              "2022-09-20T09:24:00+07:00", "end_time": "2022-09-20T09:26:00+07:00",
                                          "avg": 0},
                             {"start_time": "2022-09-20T09:26:00+07:00", "end_time": "2022-09-20T09:28:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:28:00+07:00", "end_time": "2022-09-20T09:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:32:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:32:00+07:00", "end_time": "2022-09-20T09:34:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:34:00+07:00", "end_time": "2022-09-20T09:36:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:36:00+07:00", "end_time": "2022-09-20T09:38:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:38:00+07:00", "end_time": "2022-09-20T09:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:42:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:42:00+07:00", "end_time": "2022-09-20T09:44:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:44:00+07:00", "end_time": "2022-09-20T09:46:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:46:00+07:00", "end_time": "2022-09-20T09:48:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:48:00+07:00", "end_time": "2022-09-20T09:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:52:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:52:00+07:00", "end_time": "2022-09-20T09:54:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:54:00+07:00", "end_time": "2022-09-20T09:56:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:56:00+07:00", "end_time": "2022-09-20T09:58:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:58:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                              "avg": 0}],
                          'assertion_type': 'DISABLED', 'assertion_value': '', 'is_assert_json_schema_only': False, 'exclude_keys': []
                          })

    def test_retrieve_3_hours_with_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_with_result(self, "180MIN")

        self.assertEqual(response.data,
                         {"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "180MIN",
                          "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body": None, 'previous_step_id': None,
                          'status_page_category': None, 'status_page_category_id': None, 
                          "success_rate": [
                              {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:05:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:05:00+07:00", "end_time": "2022-09-20T07:10:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:10:00+07:00", "end_time": "2022-09-20T07:15:00+07:00",
                               "success":
                                   0, "failed": 0},
                              {"start_time": "2022-09-20T07:15:00+07:00", "end_time": "2022-09-20T07:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:25:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:25:00+07:00", "end_time": "2022-09-20T07:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T07:35:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:35:00+07:00", "end_time": "2022-09-20T07:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T07:45:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:45:00+07:00", "end_time": "2022-09-20T07:50:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:50:00+07:00", "end_time": "2022-09-20T07:55:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:55:00+07:00", "end_time": "2022-09-20T08:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:05:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:05:00+07:00", "end_time": "2022-09-20T08:10:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:10:00+07:00", "end_time": "2022-09-20T08:15:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:15:00+07:00", "end_time": "2022-09-20T08:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:25:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:25:00+07:00", "end_time": "2022-09-20T08:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T08:35:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:35:00+07:00", "end_time": "2022-09-20T08:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T08:45:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:45:00+07:00", "end_time": "2022-09-20T08:50:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:50:00+07:00", "end_time": "2022-09-20T08:55:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:55:00+07:00", "end_time": "2022-09-20T09:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:05:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:05:00+07:00", "end_time": "2022-09-20T09:10:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:15:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:15:00+07:00", "end_time": "2022-09-20T09:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:25:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:25:00+07:00", "end_time": "2022-09-20T09:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:35:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:35:00+07:00", "end_time": "2022-09-20T09:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:45:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:45:00+07:00", "end_time": "2022-09-20T09:50:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:55:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:55:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                               "success": 1, "failed": 0}], "response_time": [
                             {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:05:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:05:00+07:00", "end_time": "2022-09-20T07:10:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:10:00+07:00", "end_time": "2022-09-20T07:15:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:15:00+07:00", "end_time": "2022-09-20T07:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:25:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:25:00+07:00", "end_time": "2022-09-20T07:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T07:35:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:35:00+07:00", "end_time": "2022-09-20T07:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T07:45:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:45:00+07:00", "end_time": "2022-09-20T07:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:50:00+07:00", "end_time": "2022-09-20T07:55:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:55:00+07:00", "end_time": "2022-09-20T08:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:05:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:05:00+07:00", "end_time": "2022-09-20T08:10:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:10:00+07:00", "end_time": "2022-09-20T08:15:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:15:00+07:00", "end_time": "2022-09-20T08:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:25:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:25:00+07:00", "end_time": "2022-09-20T08:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T08:35:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:35:00+07:00", "end_time": "2022-09-20T08:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T08:45:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:45:00+07:00", "end_time": "2022-09-20T08:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:50:00+07:00", "end_time": "2022-09-20T08:55:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:55:00+07:00", "end_time": "2022-09-20T09:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:05:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:05:00+07:00", "end_time": "2022-09-20T09:10:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:15:00+07:00",
                              "avg": 0}, {"start_time":
                                              "2022-09-20T09:15:00+07:00", "end_time": "2022-09-20T09:20:00+07:00",
                                          "avg": 0},
                             {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:25:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:25:00+07:00", "end_time": "2022-09-20T09:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:35:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:35:00+07:00", "end_time": "2022-09-20T09:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:45:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:45:00+07:00", "end_time": "2022-09-20T09:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:55:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:55:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                              "avg": 100}],
                          'assertion_type': 'DISABLED', 'assertion_value': '', 'is_assert_json_schema_only': False, 'exclude_keys': []
                          })

    def test_retrieve_3_hours_without_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_without_result(self, "180MIN")

        self.assertEqual(response.data,
                         {"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "180MIN",
                          "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body": None, 'previous_step_id': None,
                          'status_page_category': None, 'status_page_category_id': None, 
                          "success_rate": [
                              {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:05:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:05:00+07:00", "end_time": "2022-09-20T07:10:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:10:00+07:00", "end_time": "2022-09-20T07:15:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:15:00+07:00", "end_time": "2022-09-20T07:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:25:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:25:00+07:00", "end_time": "2022-09-20T07:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T07:35:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:35:00+07:00", "end_time": "2022-09-20T07:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T07:45:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:45:00+07:00", "end_time": "2022-09-20T07:50:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:50:00+07:00", "end_time": "2022-09-20T07:55:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:55:00+07:00", "end_time": "2022-09-20T08:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:05:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:05:00+07:00", "end_time": "2022-09-20T08:10:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:10:00+07:00", "end_time": "2022-09-20T08:15:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:15:00+07:00", "end_time": "2022-09-20T08:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:25:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:25:00+07:00", "end_time": "2022-09-20T08:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T08:35:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:35:00+07:00", "end_time": "2022-09-20T08:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T08:45:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:45:00+07:00", "end_time": "2022-09-20T08:50:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:50:00+07:00", "end_time": "2022-09-20T08:55:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:55:00+07:00", "end_time": "2022-09-20T09:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:05:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:05:00+07:00", "end_time": "2022-09-20T09:10:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:15:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:15:00+07:00", "end_time": "2022-09-20T09:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:25:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:25:00+07:00", "end_time": "2022-09-20T09:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:35:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:35:00+07:00", "end_time": "2022-09-20T09:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:45:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:45:00+07:00", "end_time": "2022-09-20T09:50:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:55:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:55:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                               "success": 0, "failed": 0}], "response_time": [
                             {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:05:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:05:00+07:00", "end_time": "2022-09-20T07:10:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:10:00+07:00", "end_time": "2022-09-20T07:15:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:15:00+07:00", "end_time": "2022-09-20T07:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:25:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:25:00+07:00", "end_time": "2022-09-20T07:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T07:35:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:35:00+07:00", "end_time": "2022-09-20T07:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T07:45:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:45:00+07:00", "end_time": "2022-09-20T07:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:50:00+07:00", "end_time": "2022-09-20T07:55:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:55:00+07:00", "end_time": "2022-09-20T08:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:05:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:05:00+07:00", "end_time": "2022-09-20T08:10:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:10:00+07:00", "end_time": "2022-09-20T08:15:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:15:00+07:00", "end_time": "2022-09-20T08:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:25:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:25:00+07:00", "end_time": "2022-09-20T08:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T08:35:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:35:00+07:00", "end_time": "2022-09-20T08:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T08:45:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:45:00+07:00", "end_time": "2022-09-20T08:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:50:00+07:00", "end_time": "2022-09-20T08:55:00+07:00",
                              "avg": 0}, {"start_time": "2022-09-20T08:55:00+07:00",
                                          "end_time": "2022-09-20T09:00:00+07:00", "avg": 0},
                             {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:05:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:05:00+07:00", "end_time": "2022-09-20T09:10:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:15:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:15:00+07:00", "end_time": "2022-09-20T09:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:25:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:25:00+07:00", "end_time": "2022-09-20T09:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:35:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:35:00+07:00", "end_time": "2022-09-20T09:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:45:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:45:00+07:00", "end_time": "2022-09-20T09:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T09:55:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:55:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                              "avg": 0}],
                          'assertion_type': 'DISABLED', 'assertion_value': '', 'is_assert_json_schema_only': False, 'exclude_keys': []
                          })

    def test_retrieve_6_hours_with_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_with_result(self, "360MIN")

        self.assertEqual(response.data,
                         {"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "360MIN",
                          "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body": None, 'previous_step_id': None,
                          'status_page_category': None, 'status_page_category_id': None, 
                          "success_rate": [
                              {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:10:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T04:10:00+07:00", "end_time": "2022-09-20T04:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T04:20:00+07:00", "end_time": "2022-09-20T04:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T04:30:00+07:00", "end_time": "2022-09-20T04:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T04:40:00+07:00", "end_time": "2022-09-20T04:50:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T04:50:00+07:00", "end_time": "2022-09-20T05:00:00+07:00",
                               "success": 0, "failed":
                                   0},
                              {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:10:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T05:10:00+07:00", "end_time": "2022-09-20T05:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T05:20:00+07:00", "end_time": "2022-09-20T05:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T05:30:00+07:00", "end_time": "2022-09-20T05:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T05:40:00+07:00", "end_time": "2022-09-20T05:50:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T05:50:00+07:00", "end_time": "2022-09-20T06:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:10:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T06:10:00+07:00", "end_time": "2022-09-20T06:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T06:20:00+07:00", "end_time": "2022-09-20T06:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T06:30:00+07:00", "end_time": "2022-09-20T06:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T06:40:00+07:00", "end_time": "2022-09-20T06:50:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T06:50:00+07:00", "end_time": "2022-09-20T07:00:00+07:00",
                               "success": 0, "failed": 0}, {"start_time": "2022-09-20T07:00:00+07:00", "end_time":
                                  "2022-09-20T07:10:00+07:00", "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:10:00+07:00", "end_time": "2022-09-20T07:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T07:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T07:50:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:50:00+07:00", "end_time": "2022-09-20T08:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:10:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:10:00+07:00", "end_time": "2022-09-20T08:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T08:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T08:50:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:50:00+07:00", "end_time": "2022-09-20T09:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:10:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:50:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                               "success": 1, "failed": 0}], "response_time": [
                             {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:10:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T04:10:00+07:00", "end_time": "2022-09-20T04:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T04:20:00+07:00", "end_time": "2022-09-20T04:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T04:30:00+07:00", "end_time": "2022-09-20T04:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T04:40:00+07:00", "end_time": "2022-09-20T04:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T04:50:00+07:00", "end_time": "2022-09-20T05:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:10:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T05:10:00+07:00", "end_time": "2022-09-20T05:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T05:20:00+07:00", "end_time": "2022-09-20T05:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T05:30:00+07:00", "end_time": "2022-09-20T05:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T05:40:00+07:00", "end_time": "2022-09-20T05:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T05:50:00+07:00", "end_time": "2022-09-20T06:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:10:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T06:10:00+07:00", "end_time": "2022-09-20T06:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T06:20:00+07:00", "end_time": "2022-09-20T06:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T06:30:00+07:00", "end_time": "2022-09-20T06:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T06:40:00+07:00", "end_time": "2022-09-20T06:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T06:50:00+07:00", "end_time": "2022-09-20T07:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:10:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:10:00+07:00", "end_time": "2022-09-20T07:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T07:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T07:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:50:00+07:00", "end_time": "2022-09-20T08:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:10:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:10:00+07:00", "end_time": "2022-09-20T08:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T08:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T08:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:50:00+07:00", "end_time": "2022-09-20T09:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:10:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                              "avg": 100}],
                          'assertion_type': 'DISABLED', 'assertion_value': '', 'is_assert_json_schema_only': False, 'exclude_keys': []
                          })

    def test_retrieve_6_hours_without_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_without_result(self, "360MIN")

        self.assertEqual(response.data,
                         {"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "360MIN",
                          "body_type": "FORM", "query_params": [], "headers": [], "body_form": [],
                          "raw_body": None, 'previous_step_id': None, 'status_page_category': None, 'status_page_category_id': None, "success_rate": [
                             {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:10:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T04:10:00+07:00", "end_time": "2022-09-20T04:20:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T04:20:00+07:00", "end_time": "2022-09-20T04:30:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T04:30:00+07:00", "end_time": "2022-09-20T04:40:00+07:00",
                              "success": 0, "failed": 0}, {"start_time": "2022-09-20T04:40:00+07:00",
                                                           "end_time": "2022-09-20T04:50:00+07:00", "success": 0,
                                                           "failed": 0},
                             {"start_time": "2022-09-20T04:50:00+07:00", "end_time": "2022-09-20T05:00:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:10:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T05:10:00+07:00", "end_time": "2022-09-20T05:20:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T05:20:00+07:00", "end_time": "2022-09-20T05:30:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T05:30:00+07:00", "end_time": "2022-09-20T05:40:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T05:40:00+07:00", "end_time": "2022-09-20T05:50:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T05:50:00+07:00", "end_time": "2022-09-20T06:00:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:10:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T06:10:00+07:00", "end_time": "2022-09-20T06:20:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T06:20:00+07:00", "end_time": "2022-09-20T06:30:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T06:30:00+07:00", "end_time": "2022-09-20T06:40:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T06:40:00+07:00", "end_time": "2022-09-20T06:50:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T06:50:00+07:00", "end_time": "2022-09-20T07:00:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:10:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T07:10:00+07:00", "end_time": "2022-09-20T07:20:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:30:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T07:40:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T07:50:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T07:50:00+07:00", "end_time": "2022-09-20T08:00:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:10:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T08:10:00+07:00", "end_time": "2022-09-20T08:20:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:30:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T08:40:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T08:50:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T08:50:00+07:00", "end_time": "2022-09-20T09:00:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:10:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:20:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:30:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:40:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:50:00+07:00",
                              "success": 0, "failed": 0},
                             {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                              "success": 0, "failed": 0}], "response_time": [
                             {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:10:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T04:10:00+07:00", "end_time": "2022-09-20T04:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T04:20:00+07:00", "end_time": "2022-09-20T04:30:00+07:00",
                              "avg": 0}, {"start_time":
                                              "2022-09-20T04:30:00+07:00", "end_time": "2022-09-20T04:40:00+07:00",
                                          "avg": 0},
                             {"start_time": "2022-09-20T04:40:00+07:00", "end_time": "2022-09-20T04:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T04:50:00+07:00", "end_time": "2022-09-20T05:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:10:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T05:10:00+07:00", "end_time": "2022-09-20T05:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T05:20:00+07:00", "end_time": "2022-09-20T05:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T05:30:00+07:00", "end_time": "2022-09-20T05:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T05:40:00+07:00", "end_time": "2022-09-20T05:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T05:50:00+07:00", "end_time": "2022-09-20T06:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:10:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T06:10:00+07:00", "end_time": "2022-09-20T06:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T06:20:00+07:00", "end_time": "2022-09-20T06:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T06:30:00+07:00", "end_time": "2022-09-20T06:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T06:40:00+07:00", "end_time": "2022-09-20T06:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T06:50:00+07:00", "end_time": "2022-09-20T07:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:10:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:10:00+07:00", "end_time": "2022-09-20T07:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T07:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T07:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:50:00+07:00", "end_time": "2022-09-20T08:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:10:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:10:00+07:00", "end_time": "2022-09-20T08:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T08:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T08:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:50:00+07:00", "end_time": "2022-09-20T09:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:10:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:10:00+07:00", "end_time": "2022-09-20T09:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T09:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T09:50:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:50:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                              "avg": 0}],
                          'assertion_type': 'DISABLED', 'assertion_value': '', 'is_assert_json_schema_only': False, 'exclude_keys': []
                          })

    def test_retrieve_12_hours_with_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_with_result(self, "720MIN")

        self.assertEqual(response.data,
                         {"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "720MIN",
                          "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body": None, 'previous_step_id': None, 
                          'status_page_category': None, 'status_page_category_id': None,
                          "success_rate": [
                              {"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T22:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T22:20:00+07:00", "end_time": "2022-09-19T22:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T22:40:00+07:00", "end_time": "2022-09-19T23:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-19T23:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T23:20:00+07:00", "end_time": "2022-09-19T23:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T23:40:00+07:00", "end_time": "2022-09-20T00:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T00:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T00:20:00+07:00", "end_time": "2022-09-20T00:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T00:40:00+07:00", "end_time": "2022-09-20T01:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T01:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T01:20:00+07:00", "end_time": "2022-09-20T01:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T01:40:00+07:00", "end_time": "2022-09-20T02:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T02:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T02:20:00+07:00", "end_time": "2022-09-20T02:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T02:40:00+07:00", "end_time": "2022-09-20T03:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T03:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T03:20:00+07:00", "end_time": "2022-09-20T03:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T03:40:00+07:00", "end_time": "2022-09-20T04:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T04:20:00+07:00", "end_time": "2022-09-20T04:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T04:40:00+07:00", "end_time": "2022-09-20T05:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T05:20:00+07:00", "end_time": "2022-09-20T05:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T05:40:00+07:00", "end_time": "2022-09-20T06:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:20:00+07:00",
                               "success":
                                   0, "failed": 0},
                              {"start_time": "2022-09-20T06:20:00+07:00", "end_time": "2022-09-20T06:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T06:40:00+07:00", "end_time": "2022-09-20T07:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T08:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T09:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                               "success": 1, "failed": 0}], "response_time": [
                             {"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T22:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T22:20:00+07:00", "end_time": "2022-09-19T22:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T22:40:00+07:00", "end_time": "2022-09-19T23:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-19T23:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T23:20:00+07:00", "end_time": "2022-09-19T23:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T23:40:00+07:00", "end_time": "2022-09-20T00:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T00:20:00+07:00", "avg":
                                 0},
                             {"start_time": "2022-09-20T00:20:00+07:00", "end_time": "2022-09-20T00:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T00:40:00+07:00", "end_time": "2022-09-20T01:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T01:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T01:20:00+07:00", "end_time": "2022-09-20T01:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T01:40:00+07:00", "end_time": "2022-09-20T02:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T02:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T02:20:00+07:00", "end_time": "2022-09-20T02:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T02:40:00+07:00", "end_time": "2022-09-20T03:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T03:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T03:20:00+07:00", "end_time": "2022-09-20T03:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T03:40:00+07:00", "end_time": "2022-09-20T04:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T04:20:00+07:00", "end_time": "2022-09-20T04:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T04:40:00+07:00", "end_time": "2022-09-20T05:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T05:20:00+07:00", "end_time": "2022-09-20T05:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T05:40:00+07:00", "end_time": "2022-09-20T06:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T06:20:00+07:00", "end_time": "2022-09-20T06:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T06:40:00+07:00", "end_time": "2022-09-20T07:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T08:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T09:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                              "avg": 100}],
                          'assertion_type': 'DISABLED', 'assertion_value': '', 'is_assert_json_schema_only': False, 'exclude_keys': []
                          })

    def test_retrieve_12_hours_without_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_without_result(self, "720MIN")

        self.assertEqual(response.data,
                         {"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "720MIN",
                          "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body": None, 'previous_step_id': None,
                          'status_page_category': None, 'status_page_category_id': None,
                          "success_rate": [
                              {"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T22:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T22:20:00+07:00", "end_time": "2022-09-19T22:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T22:40:00+07:00", "end_time": "2022-09-19T23:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-19T23:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T23:20:00+07:00", "end_time": "2022-09-19T23:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T23:40:00+07:00", "end_time": "2022-09-20T00:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T00:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T00:20:00+07:00", "end_time": "2022-09-20T00:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T00:40:00+07:00", "end_time": "2022-09-20T01:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T01:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T01:20:00+07:00", "end_time": "2022-09-20T01:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T01:40:00+07:00", "end_time": "2022-09-20T02:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T02:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T02:20:00+07:00", "end_time": "2022-09-20T02:40:00+07:00",
                               "success": 0,
                               "failed": 0},
                              {"start_time": "2022-09-20T02:40:00+07:00", "end_time": "2022-09-20T03:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T03:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T03:20:00+07:00", "end_time": "2022-09-20T03:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T03:40:00+07:00", "end_time": "2022-09-20T04:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T04:20:00+07:00", "end_time": "2022-09-20T04:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T04:40:00+07:00", "end_time": "2022-09-20T05:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T05:20:00+07:00", "end_time": "2022-09-20T05:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T05:40:00+07:00", "end_time": "2022-09-20T06:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T06:20:00+07:00", "end_time": "2022-09-20T06:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T06:40:00+07:00", "end_time": "2022-09-20T07:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T08:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T09:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:20:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:40:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                               "success": 0, "failed": 0}], "response_time": [
                             {"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T22:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T22:20:00+07:00", "end_time": "2022-09-19T22:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T22:40:00+07:00", "end_time": "2022-09-19T23:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-19T23:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T23:20:00+07:00", "end_time": "2022-09-19T23:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T23:40:00+07:00", "end_time": "2022-09-20T00:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T00:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T00:20:00+07:00", "end_time": "2022-09-20T00:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T00:40:00+07:00", "end_time": "2022-09-20T01:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T01:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T01:20:00+07:00", "end_time": "2022-09-20T01:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T01:40:00+07:00", "end_time": "2022-09-20T02:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T02:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T02:20:00+07:00", "end_time": "2022-09-20T02:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T02:40:00+07:00", "end_time": "2022-09-20T03:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T03:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T03:20:00+07:00", "end_time": "2022-09-20T03:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T03:40:00+07:00", "end_time": "2022-09-20T04:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T04:20:00+07:00", "end_time": "2022-09-20T04:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T04:40:00+07:00", "end_time": "2022-09-20T05:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T05:20:00+07:00", "end_time": "2022-09-20T05:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T05:40:00+07:00", "end_time": "2022-09-20T06:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T06:20:00+07:00", "end_time": "2022-09-20T06:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T06:40:00+07:00", "end_time": "2022-09-20T07:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:20:00+07:00", "end_time": "2022-09-20T07:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:40:00+07:00", "end_time": "2022-09-20T08:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:20:00+07:00", "end_time": "2022-09-20T08:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:40:00+07:00", "end_time": "2022-09-20T09:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:20:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:20:00+07:00", "end_time": "2022-09-20T09:40:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:40:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                              "avg": 0}],
                          'assertion_type': 'DISABLED', 'assertion_value': '', 'is_assert_json_schema_only': False, 'exclude_keys': []
                          })

    def test_retrieve_24_hours_with_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_with_result(self, "1440MIN")

        self.assertEqual(response.data,
                         {"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "1440MIN",
                          "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body": None, 'previous_step_id': None,
                          'status_page_category': None, 'status_page_category_id': None,
                          "success_rate": [
                              {"start_time": "2022-09-19T10:00:00+07:00", "end_time": "2022-09-19T10:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T10:30:00+07:00", "end_time": "2022-09-19T11:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T11:00:00+07:00", "end_time": "2022-09-19T11:30:00+07:00",
                               "success": 0,
                               "failed": 0},
                              {"start_time": "2022-09-19T11:30:00+07:00", "end_time": "2022-09-19T12:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T12:00:00+07:00", "end_time": "2022-09-19T12:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T12:30:00+07:00", "end_time": "2022-09-19T13:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T13:00:00+07:00", "end_time": "2022-09-19T13:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T13:30:00+07:00", "end_time": "2022-09-19T14:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T14:00:00+07:00", "end_time": "2022-09-19T14:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T14:30:00+07:00", "end_time": "2022-09-19T15:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T15:00:00+07:00", "end_time": "2022-09-19T15:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T15:30:00+07:00", "end_time": "2022-09-19T16:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T16:00:00+07:00", "end_time": "2022-09-19T16:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T16:30:00+07:00", "end_time": "2022-09-19T17:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T17:00:00+07:00", "end_time": "2022-09-19T17:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T17:30:00+07:00", "end_time": "2022-09-19T18:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T18:00:00+07:00", "end_time": "2022-09-19T18:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T18:30:00+07:00", "end_time": "2022-09-19T19:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T19:00:00+07:00", "end_time": "2022-09-19T19:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T19:30:00+07:00", "end_time": "2022-09-19T20:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T20:00:00+07:00", "end_time": "2022-09-19T20:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T20:30:00+07:00", "end_time": "2022-09-19T21:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T21:00:00+07:00", "end_time": "2022-09-19T21:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T21:30:00+07:00", "end_time": "2022-09-19T22:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T22:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T22:30:00+07:00", "end_time": "2022-09-19T23:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-19T23:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T23:30:00+07:00", "end_time": "2022-09-20T00:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T00:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T00:30:00+07:00", "end_time": "2022-09-20T01:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T01:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T01:30:00+07:00", "end_time": "2022-09-20T02:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T02:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T02:30:00+07:00", "end_time": "2022-09-20T03:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T03:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T03:30:00+07:00", "end_time": "2022-09-20T04:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T04:30:00+07:00", "end_time": "2022-09-20T05:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T05:30:00+07:00", "end_time": "2022-09-20T06:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T06:30:00+07:00", "end_time": "2022-09-20T07:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T08:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T09:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                               "success": 1, "failed": 0}], "response_time": [{"start_time":
                                    "2022-09-19T10:00:00+07:00",
                                "end_time": "2022-09-19T10:30:00+07:00",
                                "avg": 0}, {
                                    "start_time": "2022-09-19T10:30:00+07:00",
                                    "end_time": "2022-09-19T11:00:00+07:00",
                                    "avg": 0},
                                {
                                    "start_time": "2022-09-19T11:00:00+07:00",
                                    "end_time": "2022-09-19T11:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T11:30:00+07:00",
                                    "end_time": "2022-09-19T12:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T12:00:00+07:00",
                                    "end_time": "2022-09-19T12:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T12:30:00+07:00",
                                    "end_time": "2022-09-19T13:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T13:00:00+07:00",
                                    "end_time": "2022-09-19T13:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T13:30:00+07:00",
                                    "end_time": "2022-09-19T14:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T14:00:00+07:00",
                                    "end_time": "2022-09-19T14:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T14:30:00+07:00",
                                    "end_time": "2022-09-19T15:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T15:00:00+07:00",
                                    "end_time": "2022-09-19T15:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T15:30:00+07:00",
                                    "end_time": "2022-09-19T16:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T16:00:00+07:00",
                                    "end_time": "2022-09-19T16:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T16:30:00+07:00",
                                    "end_time": "2022-09-19T17:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T17:00:00+07:00",
                                    "end_time": "2022-09-19T17:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T17:30:00+07:00",
                                    "end_time": "2022-09-19T18:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T18:00:00+07:00",
                                    "end_time": "2022-09-19T18:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T18:30:00+07:00",
                                    "end_time": "2022-09-19T19:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T19:00:00+07:00",
                                    "end_time": "2022-09-19T19:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T19:30:00+07:00",
                                    "end_time": "2022-09-19T20:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T20:00:00+07:00",
                                    "end_time": "2022-09-19T20:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T20:30:00+07:00",
                                    "end_time": "2022-09-19T21:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T21:00:00+07:00",
                                    "end_time": "2022-09-19T21:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T21:30:00+07:00",
                                    "end_time": "2022-09-19T22:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T22:00:00+07:00",
                                    "end_time": "2022-09-19T22:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T22:30:00+07:00",
                                    "end_time": "2022-09-19T23:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T23:00:00+07:00",
                                    "end_time": "2022-09-19T23:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-19T23:30:00+07:00",
                                    "end_time": "2022-09-20T00:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-20T00:00:00+07:00",
                                    "end_time": "2022-09-20T00:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-20T00:30:00+07:00",
                                    "end_time": "2022-09-20T01:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-20T01:00:00+07:00",
                                    "end_time": "2022-09-20T01:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-20T01:30:00+07:00",
                                    "end_time": "2022-09-20T02:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-20T02:00:00+07:00",
                                    "end_time": "2022-09-20T02:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-20T02:30:00+07:00",
                                    "end_time": "2022-09-20T03:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-20T03:00:00+07:00",
                                    "end_time": "2022-09-20T03:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-20T03:30:00+07:00",
                                    "end_time": "2022-09-20T04:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-20T04:00:00+07:00",
                                    "end_time": "2022-09-20T04:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-20T04:30:00+07:00",
                                    "end_time": "2022-09-20T05:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-20T05:00:00+07:00",
                                    "end_time": "2022-09-20T05:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-20T05:30:00+07:00",
                                    "end_time": "2022-09-20T06:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-20T06:00:00+07:00",
                                    "end_time": "2022-09-20T06:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-20T06:30:00+07:00",
                                    "end_time": "2022-09-20T07:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-20T07:00:00+07:00",
                                    "end_time": "2022-09-20T07:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-20T07:30:00+07:00",
                                    "end_time": "2022-09-20T08:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-20T08:00:00+07:00",
                                    "end_time": "2022-09-20T08:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-20T08:30:00+07:00",
                                    "end_time": "2022-09-20T09:00:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-20T09:00:00+07:00",
                                    "end_time": "2022-09-20T09:30:00+07:00",
                                    "avg": 0}, {
                                    "start_time": "2022-09-20T09:30:00+07:00",
                                    "end_time": "2022-09-20T10:00:00+07:00",
                                    "avg": 100}],
                          'assertion_type': 'DISABLED', 'assertion_value': '', 'is_assert_json_schema_only': False, 'exclude_keys': []
        })

    def test_retrieve_24_hours_without_result(self):
        response = DetailListAPIMonitor.init_for_test_retrieve_without_result(self, "1440MIN")

        self.assertEqual(response.data,
                         {"id": 1, "name": "Test Monitor", "method": "GET", "url": "Test Path", "schedule": "1440MIN",
                          "body_type": "FORM", "query_params": [], "headers": [], "body_form": [], "raw_body": None, 'previous_step_id': None,
                          'status_page_category': None, 'status_page_category_id': None,
                          "success_rate": [
                              {"start_time": "2022-09-19T10:00:00+07:00", "end_time": "2022-09-19T10:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T10:30:00+07:00", "end_time": "2022-09-19T11:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T11:00:00+07:00", "end_time": "2022-09-19T11:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T11:30:00+07:00", "end_time": "2022-09-19T12:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T12:00:00+07:00", "end_time": "2022-09-19T12:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T12:30:00+07:00", "end_time": "2022-09-19T13:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T13:00:00+07:00", "end_time": "2022-09-19T13:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T13:30:00+07:00", "end_time": "2022-09-19T14:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T14:00:00+07:00", "end_time": "2022-09-19T14:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T14:30:00+07:00", "end_time": "2022-09-19T15:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T15:00:00+07:00", "end_time": "2022-09-19T15:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T15:30:00+07:00", "end_time": "2022-09-19T16:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T16:00:00+07:00", "end_time": "2022-09-19T16:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T16:30:00+07:00", "end_time": "2022-09-19T17:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T17:00:00+07:00", "end_time": "2022-09-19T17:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T17:30:00+07:00", "end_time": "2022-09-19T18:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T18:00:00+07:00", "end_time": "2022-09-19T18:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T18:30:00+07:00", "end_time": "2022-09-19T19:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T19:00:00+07:00", "end_time": "2022-09-19T19:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T19:30:00+07:00", "end_time": "2022-09-19T20:00:00+07:00",
                               "success": 0, "failed": 0}, {"start_time":
                                    "2022-09-19T20:00:00+07:00",
                                "end_time": "2022-09-19T20:30:00+07:00", "success": 0,
                                "failed": 0},
                              {"start_time": "2022-09-19T20:30:00+07:00", "end_time": "2022-09-19T21:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T21:00:00+07:00", "end_time": "2022-09-19T21:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T21:30:00+07:00", "end_time": "2022-09-19T22:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T22:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T22:30:00+07:00", "end_time": "2022-09-19T23:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-19T23:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-19T23:30:00+07:00", "end_time": "2022-09-20T00:00:00+07:00",
                               "success": 0, "failed":
                                   0},
                              {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T00:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T00:30:00+07:00", "end_time": "2022-09-20T01:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T01:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T01:30:00+07:00", "end_time": "2022-09-20T02:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T02:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T02:30:00+07:00", "end_time": "2022-09-20T03:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T03:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T03:30:00+07:00", "end_time": "2022-09-20T04:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T04:30:00+07:00", "end_time": "2022-09-20T05:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T05:30:00+07:00", "end_time": "2022-09-20T06:00:00+07:00",
                               "success": 0, "failed": 0}, {"start_time": "2022-09-20T06:00:00+07:00", "end_time":
                                  "2022-09-20T06:30:00+07:00", "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T06:30:00+07:00", "end_time": "2022-09-20T07:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T08:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T09:00:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:30:00+07:00",
                               "success": 0, "failed": 0},
                              {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                               "success": 0, "failed": 0}], "response_time": [
                             {"start_time": "2022-09-19T10:00:00+07:00", "end_time": "2022-09-19T10:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T10:30:00+07:00", "end_time": "2022-09-19T11:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T11:00:00+07:00", "end_time": "2022-09-19T11:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T11:30:00+07:00", "end_time": "2022-09-19T12:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T12:00:00+07:00", "end_time": "2022-09-19T12:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T12:30:00+07:00", "end_time": "2022-09-19T13:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T13:00:00+07:00", "end_time": "2022-09-19T13:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T13:30:00+07:00", "end_time": "2022-09-19T14:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T14:00:00+07:00", "end_time": "2022-09-19T14:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T14:30:00+07:00", "end_time": "2022-09-19T15:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T15:00:00+07:00", "end_time": "2022-09-19T15:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T15:30:00+07:00", "end_time": "2022-09-19T16:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T16:00:00+07:00", "end_time": "2022-09-19T16:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T16:30:00+07:00", "end_time": "2022-09-19T17:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T17:00:00+07:00", "end_time": "2022-09-19T17:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T17:30:00+07:00", "end_time": "2022-09-19T18:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T18:00:00+07:00", "end_time": "2022-09-19T18:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T18:30:00+07:00", "end_time": "2022-09-19T19:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T19:00:00+07:00", "end_time": "2022-09-19T19:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T19:30:00+07:00", "end_time": "2022-09-19T20:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T20:00:00+07:00", "end_time": "2022-09-19T20:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T20:30:00+07:00", "end_time": "2022-09-19T21:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T21:00:00+07:00", "end_time": "2022-09-19T21:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T21:30:00+07:00", "end_time": "2022-09-19T22:00:00+07:00",
                              "avg": 0}, {"start_time":
                                              "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T22:30:00+07:00",
                                          "avg": 0},
                             {"start_time": "2022-09-19T22:30:00+07:00", "end_time": "2022-09-19T23:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-19T23:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-19T23:30:00+07:00", "end_time": "2022-09-20T00:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T00:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T00:30:00+07:00", "end_time": "2022-09-20T01:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T01:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T01:30:00+07:00", "end_time": "2022-09-20T02:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T02:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T02:30:00+07:00", "end_time": "2022-09-20T03:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T03:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T03:30:00+07:00", "end_time": "2022-09-20T04:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T04:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T04:30:00+07:00", "end_time": "2022-09-20T05:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T05:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T05:30:00+07:00", "end_time": "2022-09-20T06:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T06:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T06:30:00+07:00", "end_time": "2022-09-20T07:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T07:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T07:30:00+07:00", "end_time": "2022-09-20T08:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T08:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T08:30:00+07:00", "end_time": "2022-09-20T09:00:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T09:30:00+07:00",
                              "avg": 0},
                             {"start_time": "2022-09-20T09:30:00+07:00", "end_time": "2022-09-20T10:00:00+07:00",
                              "avg": 0}],
                          'assertion_type': 'DISABLED', 'assertion_value': '', 'is_assert_json_schema_only': False, 'exclude_keys': []
                          })


class StatsAPIMonitor(APITestCase):
    test_url = reverse('api-monitor-stats')
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    mock_current_time = local_timezone.localize(datetime(2022, 9, 20, 10))

    def setUp(self):
        # Mock time function
        timezone.now = lambda: self.mock_current_time

    def test_stats_with_result(self):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        monitor = APIMonitor.objects.create(
            team=team,
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

        response = self.client.get(self.test_url, format="json", **header)
        self.assertEqual(response.data, {"success_rate": [
            {"start_time": "2022-09-19T10:00:00+07:00", "end_time": "2022-09-19T11:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T11:00:00+07:00", "end_time": "2022-09-19T12:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T12:00:00+07:00", "end_time": "2022-09-19T13:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T13:00:00+07:00", "end_time": "2022-09-19T14:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T14:00:00+07:00", "end_time": "2022-09-19T15:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T15:00:00+07:00", "end_time": "2022-09-19T16:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T16:00:00+07:00", "end_time": "2022-09-19T17:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T17:00:00+07:00", "end_time": "2022-09-19T18:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T18:00:00+07:00", "end_time": "2022-09-19T19:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T19:00:00+07:00", "end_time": "2022-09-19T20:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T20:00:00+07:00", "end_time": "2022-09-19T21:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T21:00:00+07:00", "end_time": "2022-09-19T22:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T23:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-20T00:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T01:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T02:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T03:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T04:00:00+07:00", "success": 0,
             "failed": 0}, {"start_time": "2022-09-20T04:00:00+07:00",
                            "end_time": "2022-09-20T05:00:00+07:00", "success": 0, "failed": 0},
            {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T06:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T07:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "success": 1,
             "failed": 0}], "response_time": [
            {"start_time": "2022-09-19T10:00:00+07:00", "end_time": "2022-09-19T11:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T11:00:00+07:00", "end_time": "2022-09-19T12:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T12:00:00+07:00", "end_time": "2022-09-19T13:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T13:00:00+07:00", "end_time": "2022-09-19T14:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T14:00:00+07:00", "end_time": "2022-09-19T15:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T15:00:00+07:00", "end_time": "2022-09-19T16:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T16:00:00+07:00", "end_time": "2022-09-19T17:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T17:00:00+07:00", "end_time": "2022-09-19T18:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T18:00:00+07:00", "end_time": "2022-09-19T19:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T19:00:00+07:00", "end_time": "2022-09-19T20:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T20:00:00+07:00", "end_time": "2022-09-19T21:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T21:00:00+07:00", "end_time": "2022-09-19T22:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T23:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-20T00:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T01:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T02:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T03:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T04:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T05:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T06:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T07:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "avg": 100}]})

    def test_stats_without_result(self):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        monitor = APIMonitor.objects.create(
            team=team,
            name='Test Monitor',
            method='GET',
            url='Test Path',
            schedule='1440MIN',
            body_type='FORM',
        )

        response = self.client.get(self.test_url, format="json", **header)
        self.assertEqual(response.data, {"success_rate": [
            {"start_time": "2022-09-19T10:00:00+07:00", "end_time": "2022-09-19T11:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T11:00:00+07:00", "end_time": "2022-09-19T12:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T12:00:00+07:00", "end_time": "2022-09-19T13:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T13:00:00+07:00", "end_time": "2022-09-19T14:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T14:00:00+07:00", "end_time": "2022-09-19T15:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T15:00:00+07:00", "end_time": "2022-09-19T16:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T16:00:00+07:00", "end_time": "2022-09-19T17:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T17:00:00+07:00", "end_time": "2022-09-19T18:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T18:00:00+07:00", "end_time": "2022-09-19T19:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T19:00:00+07:00", "end_time": "2022-09-19T20:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T20:00:00+07:00", "end_time": "2022-09-19T21:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T21:00:00+07:00", "end_time": "2022-09-19T22:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T23:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-20T00:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T01:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T02:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T03:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T04:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T05:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T06:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T07:00:00+07:00", "success": 0,
             "failed": 0}, {"start_time": "2022-09-20T07:00:00+07:00", "end_time":
                "2022-09-20T08:00:00+07:00", "success": 0, "failed": 0},
            {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "success": 0,
             "failed": 0},
            {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "success": 0,
             "failed": 0}], "response_time": [
            {"start_time": "2022-09-19T10:00:00+07:00", "end_time": "2022-09-19T11:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T11:00:00+07:00", "end_time": "2022-09-19T12:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T12:00:00+07:00", "end_time": "2022-09-19T13:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T13:00:00+07:00", "end_time": "2022-09-19T14:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T14:00:00+07:00", "end_time": "2022-09-19T15:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T15:00:00+07:00", "end_time": "2022-09-19T16:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T16:00:00+07:00", "end_time": "2022-09-19T17:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T17:00:00+07:00", "end_time": "2022-09-19T18:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T18:00:00+07:00", "end_time": "2022-09-19T19:00:00+07:00",
             "avg": 0}, {"start_time": "2022-09-19T19:00:00+07:00", "end_time": "2022-09-19T20:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T20:00:00+07:00", "end_time": "2022-09-19T21:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T21:00:00+07:00", "end_time": "2022-09-19T22:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T22:00:00+07:00", "end_time": "2022-09-19T23:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-19T23:00:00+07:00", "end_time": "2022-09-20T00:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-20T00:00:00+07:00", "end_time": "2022-09-20T01:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-20T01:00:00+07:00", "end_time": "2022-09-20T02:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-20T02:00:00+07:00", "end_time": "2022-09-20T03:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-20T03:00:00+07:00", "end_time": "2022-09-20T04:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-20T04:00:00+07:00", "end_time": "2022-09-20T05:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-20T05:00:00+07:00", "end_time": "2022-09-20T06:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-20T06:00:00+07:00", "end_time": "2022-09-20T07:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-20T07:00:00+07:00", "end_time": "2022-09-20T08:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-20T08:00:00+07:00", "end_time": "2022-09-20T09:00:00+07:00", "avg": 0},
            {"start_time": "2022-09-20T09:00:00+07:00", "end_time": "2022-09-20T10:00:00+07:00", "avg": 0}]})


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
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        response = self.client.get(self.test_url, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_when_authenticated_and_non_empty_monitor_then_return_success_with_monitor(self):
        # Create dummy user and authenticate
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        monitor = APIMonitor.objects.create(
            team=team,
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
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        monitor = APIMonitor.objects.create(
            team=team,
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
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        # Create an API Monitor object under their account
        monitor = APIMonitor.objects.create(
            team=team,
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
        target_monitor_id = APIMonitor.objects.filter(team=team)[:1].get().id
        delete_test_path = reverse('api-monitor-detail', kwargs={'pk': target_monitor_id})

        # Object is deleted
        self.client.delete(delete_test_path, format='json', **header)
        self.assertEqual(APIMonitor.objects.all().count(), 0)
        self.assertEqual(APIMonitorResult.objects.all().count(), 0)

    def test_non_owner_cannot_delete_another_owned_api_monitor(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        # Create an API Monitor object under their account
        monitor = APIMonitor.objects.create(
            team=team,
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
        team2 = Team.objects.create(name='test team')
        team_member2 = TeamMember.objects.create(team=team2, user=malicious_user)
        
        token2 = MonAPIToken.objects.create(team_member=team_member2)
        header2 = {'HTTP_AUTHORIZATION': f"Token {token2.key}"}

        # Get path
        target_monitor_id = APIMonitor.objects.filter(team=team)[:1].get().id
        delete_test_path = reverse('api-monitor-detail', kwargs={'pk': target_monitor_id})

        # Request failed, api monitor is not deleted
        response = self.client.delete(delete_test_path, format='json', **header2)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(APIMonitor.objects.all().count(), 1)

    def test_user_can_create_new_api_monitor(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
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
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
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
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
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
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
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
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
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
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
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

    def test_user_can_create_api_monitor_without_previous_step(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Name',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'EMPTY',
        }

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(APIMonitor.objects.all().count(), 1)
        self.assertEqual(response.data,
            {
                "id": 1,
                "name": "Test Name",
                "method": "GET",
                "url": "Test Path",
                "schedule": "10MIN",
                "body_type": "EMPTY",
                "query_params": [],
                "headers": [],
                "body_form": [],
                "raw_body": None,
                "previous_step_id": None,
                "assertion_type": "DISABLED",
                "assertion_value": "",
                "is_assert_json_schema_only": False,
                "exclude_keys": [],
                "status_page_category_id": None,
            }
        )

    def test_user_can_create_api_monitor_with_empty_previous_step(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Name',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'previous_step_id': '',
            'body_type': 'EMPTY',
        }

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'previous_step_id': monitor_value['previous_step_id'],
            'body_type': monitor_value['body_type'],
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(APIMonitor.objects.all().count(), 1)
        self.assertEqual(response.data,
            {
                "id": 1,
                "name": "Test Name",
                "method": "GET",
                "url": "Test Path",
                "schedule": "10MIN",
                "body_type": "EMPTY",
                "query_params": [],
                "headers": [],
                "body_form": [],
                "raw_body": None,
                "previous_step_id": None,
                "assertion_type": "DISABLED",
                "assertion_value": "",
                "is_assert_json_schema_only": False,
                "exclude_keys": [],
                "status_page_category_id": None,
            }
        )

    def test_user_can_create_api_monitor_with_valid_previous_step(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'previous_step_id': 1,
            'body_type': 'EMPTY',
        }

        received_json_1 = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
        }

        # Expected JSON from frontend
        received_json_2 = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'previous_step_id': monitor_value['previous_step_id'],
            'body_type': monitor_value['body_type'],
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        self.client.post(create_new_monitor_test_path, data=received_json_1, format='json', **header)
        response = self.client.post(create_new_monitor_test_path, data=received_json_2, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(APIMonitor.objects.all().count(), 2)
        self.assertEqual(response.data,
            {
                "id": 2,
                "name": "Test Monitor",
                "method": "GET",
                "url": "Test Path",
                "schedule": "10MIN",
                "body_type": "EMPTY",
                "query_params": [],
                "headers": [],
                "body_form": [],
                "raw_body": None,
                "previous_step_id": 1,
                "assertion_type": "DISABLED",
                "assertion_value": "",
                "is_assert_json_schema_only": False,
                "exclude_keys": [],
                "status_page_category_id": None,
            }
        )
        
    def test_user_cannot_create_api_monitor_with_other_user_previous_step_id(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        
        user_two = User.objects.create_user(username="test2@test.com", email="test2@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user_two)
        
        token_two = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        header_two = {'HTTP_AUTHORIZATION': f"Token {token_two.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'previous_step_id': 1,
            'body_type': 'EMPTY',
        }

        received_json_1 = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
        }

        # Expected JSON from frontend
        received_json_2 = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'previous_step_id': monitor_value['previous_step_id'],
            'body_type': monitor_value['body_type'],
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        self.client.post(create_new_monitor_test_path, data=received_json_1, format='json', **header)
        response = self.client.post(create_new_monitor_test_path, data=received_json_2, format='json', **header_two)
        self.assertEqual(APIMonitor.objects.all().count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Please make sure your [previous step id] is valid and exist!")
                
                            
    def test_user_can_create_api_monitor_with_invalid_previous_step_1(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'previous_step_id': -1,
            'body_type': 'EMPTY',
        }

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'previous_step_id': monitor_value['previous_step_id'],
            'body_type': monitor_value['body_type'],
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Please make sure your [previous step id] is valid and exist!")
        self.assertEqual(APIMonitor.objects.all().count(), 0)
        
    def test_user_can_create_api_monitor_with_valid_statuspage_category_id(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        statuspage_category = StatusPageCategory.objects.create(team=team, name='category')
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'EMPTY',
            'status_page_category_id': statuspage_category.id,
        }
        
        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'status_page_category_id': monitor_value['status_page_category_id'],
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(APIMonitor.objects.all().count(), 1)
        self.assertEqual(response.data,
            {
                "id": 1,
                "name": "Test Monitor",
                "method": "GET",
                "url": "Test Path",
                "schedule": "10MIN",
                "body_type": "EMPTY",
                "query_params": [],
                "headers": [],
                "body_form": [],
                "raw_body": None,
                "previous_step_id": None,
                "assertion_type": "DISABLED",
                "assertion_value": "",
                "is_assert_json_schema_only": False,
                "exclude_keys": [],
                "status_page_category_id": statuspage_category.id,
            }
        )
        
    def test_user_cannot_create_api_monitor_with_other_user_status_page_id(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        
        user_two = User.objects.create_user(username="test2@test.com", email="test2@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user_two)
        
        status_page = StatusPageCategory.objects.create(team=team, name='category2')

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'EMPTY',
            'status_page_category_id': status_page.id,
        }

        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'status_page_category_id': monitor_value['status_page_category_id'],
        }

        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(APIMonitor.objects.all().count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Please make sure your [status page category] is valid and exist!")
                
                            
    def test_user_can_create_api_monitor_with_invalid_status_page_category(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'status_page_category_id': -1,
            'body_type': 'EMPTY',
        }

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'status_page_category_id': monitor_value['status_page_category_id'],
            'body_type': monitor_value['body_type'],
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Please make sure your [status page category] is valid and exist!")
        self.assertEqual(APIMonitor.objects.all().count(), 0)

    def test_user_can_create_api_monitor_with_invalid_previous_step_2(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'previous_step_id': "-1123j21kldsa",
            'body_type': 'EMPTY',
        }

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'previous_step_id': monitor_value['previous_step_id'],
            'body_type': monitor_value['body_type'],
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Please make sure your [previous step id] is valid and exist!")
        self.assertEqual(APIMonitor.objects.all().count(), 0)

    def test_bad_monitor_data_shouldnt_be_created(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
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
        self.assertEqual(response.data['error'],
                         "['Please make sure your [name, method, url, schedule, body_type] is valid']")

    def test_query_params_is_not_valid(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
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
        self.assertEqual(response.data['error'],
                         "['Please make sure your [query params] key and value are valid strings!']")

    def test_header_is_not_valid(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
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
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
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
    
    def test_user_can_create_new_api_monitor_with_text_assertion(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'FORM',
            "assertion_type":"TEXT",
            "assertion_value": "value",
            "is_assert_json_schema_only": False,
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
            'assertion_type': monitor_value['assertion_type'],
            "assertion_value": monitor_value['assertion_value'],
            "is_assert_json_schema_only": monitor_value['is_assert_json_schema_only'],
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(APIMonitor.objects.all().count(), 1)

    def test_user_can_create_new_api_monitor_with_json_assertion(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'EMPTY',
            "assertion_type":"JSON",
            "assertion_value": "{\"key\":\"value\"}",
            "is_assert_json_schema_only": False,
        }

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'assertion_type': monitor_value['assertion_type'],
            "assertion_value": monitor_value['assertion_value'],
            "is_assert_json_schema_only": monitor_value['is_assert_json_schema_only'],
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(APIMonitor.objects.all().count(), 1)

    def test_user_can_create_new_api_monitor_with_json_assertion_with_exclude_keys(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'EMPTY',
            "assertion_type":"JSON",
            "assertion_value": "{\"key\":\"value\", \"key2\":\"value2\"}",
            "is_assert_json_schema_only": True,
        }

        assertion_exclude_keys = [
            {
                'key': 'key1',
            },
            {
                'key': 'key2',
            }
        ]

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'assertion_type': monitor_value['assertion_type'],
            "assertion_value": monitor_value['assertion_value'],
            "is_assert_json_schema_only": monitor_value['is_assert_json_schema_only'],
            "exclude_keys": assertion_exclude_keys,
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(APIMonitor.objects.all().count(), 1)
        self.assertEqual(AssertionExcludeKey.objects.all().count(), 2)

    def test_user_can_create_new_api_monitor_with_json_assertion_schema_only(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'EMPTY',
            "assertion_type":"JSON",
            "assertion_value": "{\"key\":\"value\", \"key2\":\"value2\"}",
            "is_assert_json_schema_only": True,
        }

        assertion_exclude_keys = [
            {
                'key': 'key1',
            },
        ]

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'assertion_type': monitor_value['assertion_type'],
            "assertion_value": monitor_value['assertion_value'],
            "is_assert_json_schema_only": monitor_value['is_assert_json_schema_only'],
            "exclude_keys": assertion_exclude_keys,
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(APIMonitor.objects.all().count(), 1)
        self.assertEqual(AssertionExcludeKey.objects.all().count(), 1)

    def test_user_can_create_new_api_monitor_with_disabled_assertion(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'EMPTY',
            "assertion_type":"DISABLED",
        }

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'assertion_type': monitor_value['assertion_type'],
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(APIMonitor.objects.all().count(), 1)
        self.assertEqual(AssertionExcludeKey.objects.all().count(), 0)

    def test_exclude_keys_assertion_is_not_valid(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'EMPTY',
            'assertion_type': 'JSON',
            "assertion_value": "{\"key\":\"value\", \"key2\":\"value2\"}",
            "is_assert_json_schema_only": False,
        }

        assertion_exclude_keys = [
            {
                'key': ['key1'],
            },
        ]

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'assertion_type': monitor_value['assertion_type'],
            "assertion_value": monitor_value['assertion_value'],
            "is_assert_json_schema_only": monitor_value['is_assert_json_schema_only'],
            'exclude_keys': assertion_exclude_keys,
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "['Please make sure your [exclude key] valid strings!']")

    def test_failed_attempt_because_exclude_keys_doesnt_create_object(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'EMPTY',
            'assertion_type': 'JSON',
            "assertion_value": "{\"key\":\"value\", \"key2\":\"value2\"}",
            "is_assert_json_schema_only": False,
        }

        assertion_exclude_keys = [
            {
                'corrupted': 'key1',
            },
        ]

        # Expected JSON from frontend
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'assertion_type': monitor_value['assertion_type'],
            "assertion_value": monitor_value['assertion_value'],
            "is_assert_json_schema_only": monitor_value['is_assert_json_schema_only'],
            'exclude_keys': assertion_exclude_keys,
        }

        # Get path
        create_new_monitor_test_path = reverse('api-monitor-list')
        response = self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "['Please make sure you submit correct [exclude key]']")

class EditAPIMonitor(APITestCase):
    # PBI-15-edit-api-monitor-backend
    def test_user_can_edit_api_monitor_simple(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
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

        target_monitor_id = APIMonitor.objects.filter(team=team)[:1].get().id
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

    def test_user_can_edit_api_monitor_simple_body_form(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
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
            'body_type': 'FORM',
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
        monitorbodyform_value = [
            {
                'key': 'body form key UPDATED',
                'value': 'body form value UPDATED'
            }
        ]
        monitorrawbody_value = "This doesn't matter since body type is RAW"

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

        target_monitor_id = APIMonitor.objects.filter(team=team)[:1].get().id
        edit_monitor_path = reverse('api-monitor-detail', kwargs={'pk': target_monitor_id})
        response = self.client.put(edit_monitor_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'UPDATED Test Monitor')
        self.assertEqual(response.data['method'], 'POST')
        self.assertEqual(response.data['url'], 'Test Path')
        self.assertEqual(response.data['schedule'], '30MIN')
        self.assertEqual(response.data['body_type'], 'FORM')
        self.assertEqual(len(response.data['query_params']), 1)
        self.assertEqual(len(response.data['headers']), 2)
        self.assertEqual(len(response.data['body_form']), 1)
        self.assertEqual(response.data['raw_body'], None)

    def test_user_can_edit_api_monitor_without_optional_params(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
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
            'body_type': 'FORM',
        }
        monitorbodyform_value = [
            {
                'key': 'body form key UPDATED',
                'value': 'body form value UPDATED'
            }
        ]

        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'body_form': monitorbodyform_value
        }

        target_monitor_id = APIMonitor.objects.filter(team=team)[:1].get().id
        edit_monitor_path = reverse('api-monitor-detail', kwargs={'pk': target_monitor_id})
        response = self.client.put(edit_monitor_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'UPDATED Test Monitor')
        self.assertEqual(response.data['method'], 'POST')
        self.assertEqual(response.data['url'], 'Test Path')
        self.assertEqual(response.data['schedule'], '30MIN')
        self.assertEqual(response.data['body_type'], 'FORM')
        self.assertEqual(len(response.data['query_params']), 0)
        self.assertEqual(len(response.data['headers']), 0)
        self.assertEqual(len(response.data['body_form']), 1)
        self.assertEqual(response.data['raw_body'], None)

    def test_user_can_not_edit_api_monitor_without_required_fields(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
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
            'url': 'Test Path',
            'schedule': '30MIN',
            'body_type': 'FORM',
        }
        monitorbodyform_value = [
            {
                'key': 'body form key UPDATED',
                'value': 'body form value UPDATED'
            }
        ]

        received_json = {
            'name': monitor_value['name'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'body_form': monitorbodyform_value
        }

        target_monitor_id = APIMonitor.objects.filter(team=team)[:1].get().id
        edit_monitor_path = reverse('api-monitor-detail', kwargs={'pk': target_monitor_id})
        response = self.client.put(edit_monitor_path, data=received_json, format='json', **header)
        self.assertEqual(response.data['error'],
                         "['Please make sure your [name, method, url, schedule, body_type] is valid']")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_edit_assertion_fields(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        monitor_value = {
            'user': 'test@test.com',
            'name': 'Test Monitor',
            'method': 'GET',
            'url': 'Test Path',
            'schedule': '10MIN',
            'body_type': 'RAW',
            "assertion_type": "JSON",
            "assertion_value": "{\"test\":\"hao\"}",
            "is_assert_json_schema_only": True,
            "exclude_keys": [
                {
                    "key": "test"
                }
            ]
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

        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'assertion_type': monitor_value['assertion_type'],
            'assertion_value': monitor_value['assertion_value'],
            'is_assert_json_schema_only': monitor_value['is_assert_json_schema_only'],
            'exclude_keys': monitor_value['exclude_keys'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value
        }

        # 1. Create Object
        create_new_monitor_test_path = reverse('api-monitor-list')
        self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)

        # 2. Update Object
        received_json = {
            'name': monitor_value['name'],
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'schedule': monitor_value['schedule'],
            'body_type': monitor_value['body_type'],
            'assertion_type': monitor_value['assertion_type'],
            'assertion_value': monitor_value['assertion_value'],
            'is_assert_json_schema_only': monitor_value['is_assert_json_schema_only'],
            # 'exclude_keys': monitor_value['exclude_keys'], # Exclude keys removed
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value
        }
        target_monitor_id = APIMonitor.objects.filter(team=team)[:1].get().id
        edit_monitor_path = reverse('api-monitor-detail', kwargs={'pk': target_monitor_id})
        response = self.client.put(edit_monitor_path, data=received_json, format='json', **header)
        self.assertEqual(len(response.data['exclude_keys']), 0)

        received_json['exclude_keys'] = [
            {
                'key': 'test'
            },
            {
                'key': 'future key'
            }
        ]
        response = self.client.put(edit_monitor_path, data=received_json, format='json', **header)
        self.assertEqual(len(response.data['exclude_keys']), 2)

    def test_user_can_edit_previous_step(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
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

        # 1. Create Object id = 1
        create_new_monitor_test_path = reverse('api-monitor-list')
        self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)

        # 2. Create Object id = 2
        received_json['name'] = 'Test Monitor 2'
        self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)

        # 3. Edit object id = 2's prev step to 1
        received_json['previous_step_id'] = 1
        target_monitor_id = APIMonitor.objects.filter(team=team)[1].id
        edit_monitor_path = reverse('api-monitor-detail', kwargs={'pk': target_monitor_id})
        response = self.client.put(edit_monitor_path, data=received_json, format='json', **header)
        self.assertEqual(response.data['id'], 2)
        self.assertEqual(response.data['previous_step_id'], 1)

    def test_user_must_put_valid_previous_step(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
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

        # 1. Create Object id = 1
        create_new_monitor_test_path = reverse('api-monitor-list')
        self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)

        # 2. Create Object id = 2
        received_json['name'] = 'Test Monitor 2'
        self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)

        # 3. Edit object id = 2's prev step to "abc" --> invalid prev_step_id
        received_json['previous_step_id'] = "abc"
        target_monitor_id = APIMonitor.objects.filter(team=team)[1].id
        edit_monitor_path = reverse('api-monitor-detail', kwargs={'pk': target_monitor_id})
        response = self.client.put(edit_monitor_path, data=received_json, format='json', **header)
        self.assertEqual(response.data['error'], ['Please make sure your [previous step id] is valid and exist!'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_user_can_edit_status_page_category(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
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

        # 1. Create Object id = 1
        create_new_monitor_test_path = reverse('api-monitor-list')
        self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)

        # 2. Create  Status Page Category
        status_page_category = StatusPageCategory.objects.create(team=team, name='category')

        # 3. Edit object id = 1 status page
        received_json['status_page_category_id'] = status_page_category.id
        target_monitor_id = APIMonitor.objects.filter(team=team)[0].id
        edit_monitor_path = reverse('api-monitor-detail', kwargs={'pk': target_monitor_id})
        response = self.client.put(edit_monitor_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status_page_category_id'], status_page_category.id)

    def test_user_input_invalid_status_page_category_then_return_error(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
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

        # 1. Create Object id = 1
        create_new_monitor_test_path = reverse('api-monitor-list')
        self.client.post(create_new_monitor_test_path, data=received_json, format='json', **header)

        # 2. Create  Status Page Category
        status_page_category = StatusPageCategory.objects.create(team=team, name='category')

        # 3. Edit object id = 1 status page
        received_json['status_page_category_id'] = '999'
        target_monitor_id = APIMonitor.objects.filter(team=team)[0].id
        edit_monitor_path = reverse('api-monitor-detail', kwargs={'pk': target_monitor_id})
        response = self.client.put(edit_monitor_path, data=received_json, format='json', **header)
        self.assertEqual(response.data['error'], ['Please make sure your [status page category] is valid and exist!'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TeamMigrationsTest(MigratorTestCase):
    migrate_from = ('apimonitor', '0013_merge_20221106_1259')
    migrate_to = ('apimonitor', '0014_remove_alertsconfiguration_user_and_more')

    def prepare(self):
        """Prepare some data before the migration."""
        User = self.old_state.apps.get_model('auth', 'User')
        user = User.objects.create_user(username='test', email='test@test.com', password='test123', last_login=timezone.now())
        APIMonitor = self.old_state.apps.get_model('apimonitor', 'APIMonitor')
        APIMonitor.objects.create(
            user=user,
            name='Test Monitor',
            method='GET',
            url='Test Path',
            schedule='1MIN',
            body_type='FORM',
        )
        
        AlertsConfiguration = self.old_state.apps.get_model('apimonitor', 'AlertsConfiguration')
        AlertsConfiguration.objects.create(user=user, is_slack_active=True)
        

    def test_migration_to_team(self):
        Team = self.new_state.apps.get_model('login', 'Team')
        team = Team.objects.all()
        self.assertEqual(len(team), 1)
        self.assertEqual(team[0].name, 'Test')
        
        APIMonitor = self.new_state.apps.get_model('apimonitor', 'APIMonitor')
        apimonitor = APIMonitor.objects.all()
        self.assertEqual(len(apimonitor), 1)
        self.assertEqual(apimonitor[0].team, team[0])

        AlertsConfiguration = self.new_state.apps.get_model('apimonitor', 'AlertsConfiguration')
        alertsconfiguration = AlertsConfiguration.objects.all()
        self.assertEqual(len(alertsconfiguration), 1)
        self.assertEqual(alertsconfiguration[0].team, team[0])
