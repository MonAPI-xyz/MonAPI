from django.test import TestCase
from django.conf import settings
from django.utils import timezone
from django.core.management import call_command
from django.contrib.auth.models import User
from unittest.mock import patch
from io import StringIO
from datetime import datetime
import pytz
import requests

from apimonitor.models import APIMonitor, APIMonitorBodyForm, APIMonitorHeader, APIMonitorQueryParam, APIMonitorRawBody, APIMonitorResult


class MockResponse:
    def __init__(self, response, status_code):
        self.status_code = status_code
        self.content = response.encode('utf-8')


def mocked_request_get(*args, **kwargs):
    return MockResponse("{\"key\": \"value\"}", 200)


def mocked_request_get_exception(*args, **kwargs):
    raise requests.exceptions.Timeout("Request timed out.")


class CronManagementCommand(TestCase):
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    mock_current_time = local_timezone.localize(datetime(2022,9,20,10))
    
    def setUp(self):
        # Mock time function
        timezone.now = lambda: self.mock_current_time
        timezone.localtime = lambda: self.mock_current_time
    
    def call_command(self, *args, **kwargs):
        out = StringIO()
        call_command(
            "run_cron",
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs,
        )
        return out.getvalue()
    
    # Mock time sleep to interrupt on each iteration
    @patch("time.sleep", side_effect=InterruptedError)
    def test_when_not_exists_api_monitor_then_no_change(self, *args):
        try:
            self.call_command()
        except InterruptedError:
            pass
        
        result = APIMonitorResult.objects.count()
        self.assertEqual(result, 0)
        
    @patch("time.sleep", side_effect=InterruptedError)
    def test_when_result_exists_in_given_interval_then_continue(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='EMPTY',
        )
        
        APIMonitorResult.objects.create(
            monitor=monitor,
            execution_time=self.mock_current_time,
            date=self.mock_current_time.date(),
            hour=self.mock_current_time.hour,
            minute=self.mock_current_time.minute,
            response_time=10,
            success=True,
            log_response='resp',
            log_error='error',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        
        
        count = APIMonitorResult.objects.count()
        self.assertEqual(count, 1)
        
    @patch("time.sleep", side_effect=InterruptedError)
    @patch("requests.get", mocked_request_get)
    def test_when_result_not_exists_in_given_interval_and_empty_body_then_run_test(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='EMPTY',
        )
        
        APIMonitorHeader.objects.create(
            monitor=monitor,
            key='header key',
            value='header value',
        )
        
        APIMonitorQueryParam.objects.create(
            monitor=monitor,
            key='query key',
            value='query value',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        
        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].date, self.mock_current_time.date())
        self.assertEqual(result[0].hour, self.mock_current_time.hour)
        self.assertEqual(result[0].minute, self.mock_current_time.minute)
        self.assertEqual(result[0].success, True)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, '')
        
        
    @patch("time.sleep", side_effect=InterruptedError)
    @patch("requests.get", mocked_request_get)
    def test_when_result_not_exists_in_given_interval_and_form_body_then_run_test(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='FORM',
        )
        
        APIMonitorHeader.objects.create(
            monitor=monitor,
            key='header key',
            value='header value',
        )
        
        APIMonitorBodyForm.objects.create(
            monitor=monitor,
            key='form key',
            value='form value',
        )
        
        APIMonitorQueryParam.objects.create(
            monitor=monitor,
            key='query key',
            value='query value',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        
        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].date, self.mock_current_time.date())
        self.assertEqual(result[0].hour, self.mock_current_time.hour)
        self.assertEqual(result[0].minute, self.mock_current_time.minute)
        self.assertEqual(result[0].success, True)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, '')
        
        
    @patch("time.sleep", side_effect=InterruptedError)
    @patch("requests.get", mocked_request_get)
    def test_when_result_not_exists_in_given_interval_and_raw_body_then_run_test(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='RAW',
        )
        
        APIMonitorHeader.objects.create(
            monitor=monitor,
            key='header key',
            value='header value',
        )
        
        APIMonitorRawBody.objects.create(
            monitor=monitor,
            body='{}'
        )
        
        APIMonitorQueryParam.objects.create(
            monitor=monitor,
            key='query key',
            value='query value',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        
        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].date, self.mock_current_time.date())
        self.assertEqual(result[0].hour, self.mock_current_time.hour)
        self.assertEqual(result[0].minute, self.mock_current_time.minute)
        self.assertEqual(result[0].success, True)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, '')
        
        
    @patch("time.sleep", side_effect=InterruptedError)
    @patch("requests.get", mocked_request_get)
    def test_when_result_not_exists_in_given_interval_and_raw_body_not_exists_then_run_test(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='RAW',
        )
        
        APIMonitorHeader.objects.create(
            monitor=monitor,
            key='header key',
            value='header value',
        )
        
        APIMonitorQueryParam.objects.create(
            monitor=monitor,
            key='query key',
            value='query value',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        
        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].date, self.mock_current_time.date())
        self.assertEqual(result[0].hour, self.mock_current_time.hour)
        self.assertEqual(result[0].minute, self.mock_current_time.minute)
        self.assertEqual(result[0].success, True)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, '')
        
        
    @patch("time.sleep", side_effect=InterruptedError)
    @patch("requests.get", mocked_request_get_exception)
    def test_when_result_not_exists_in_given_interval_and_error_exception_then_log_exception(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='RAW',
        )
        
        APIMonitorHeader.objects.create(
            monitor=monitor,
            key='header key',
            value='header value',
        )
        
        APIMonitorQueryParam.objects.create(
            monitor=monitor,
            key='query key',
            value='query value',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        
        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].date, self.mock_current_time.date())
        self.assertEqual(result[0].hour, self.mock_current_time.hour)
        self.assertEqual(result[0].minute, self.mock_current_time.minute)
        self.assertEqual(result[0].success, False)
        self.assertEqual(result[0].log_response, "")
        self.assertEqual(result[0].log_error, 'Request timed out.')
        
           
    @patch("time.sleep", side_effect=InterruptedError)
    @patch("requests.post", mocked_request_get)
    def test_when_method_post_and_result_not_exists_in_given_interval_then_run_test(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='POST',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='RAW',
        )
        
        APIMonitorHeader.objects.create(
            monitor=monitor,
            key='header key',
            value='header value',
        )
        
        APIMonitorQueryParam.objects.create(
            monitor=monitor,
            key='query key',
            value='query value',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        
        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].date, self.mock_current_time.date())
        self.assertEqual(result[0].hour, self.mock_current_time.hour)
        self.assertEqual(result[0].minute, self.mock_current_time.minute)
        self.assertEqual(result[0].success, True)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, '')
        
        
    @patch("time.sleep", side_effect=InterruptedError)
    @patch("requests.patch", mocked_request_get)
    def test_when_method_patch_and_result_not_exists_in_given_interval_then_run_test(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='PATCH',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='RAW',
        )
        
        APIMonitorHeader.objects.create(
            monitor=monitor,
            key='header key',
            value='header value',
        )
        
        APIMonitorQueryParam.objects.create(
            monitor=monitor,
            key='query key',
            value='query value',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        
        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].date, self.mock_current_time.date())
        self.assertEqual(result[0].hour, self.mock_current_time.hour)
        self.assertEqual(result[0].minute, self.mock_current_time.minute)
        self.assertEqual(result[0].success, True)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, '')
        
        
    @patch("time.sleep", side_effect=InterruptedError)
    @patch("requests.put", mocked_request_get)
    def test_when_method_put_and_result_not_exists_in_given_interval_then_run_test(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='PUT',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='RAW',
        )
        
        APIMonitorHeader.objects.create(
            monitor=monitor,
            key='header key',
            value='header value',
        )
        
        APIMonitorQueryParam.objects.create(
            monitor=monitor,
            key='query key',
            value='query value',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        
        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].date, self.mock_current_time.date())
        self.assertEqual(result[0].hour, self.mock_current_time.hour)
        self.assertEqual(result[0].minute, self.mock_current_time.minute)
        self.assertEqual(result[0].success, True)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, '')
        
        
    @patch("time.sleep", side_effect=InterruptedError)
    @patch("requests.delete", mocked_request_get)
    def test_when_method_delete_and_result_not_exists_in_given_interval_then_run_test(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='DELETE',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='RAW',
        )
        
        APIMonitorHeader.objects.create(
            monitor=monitor,
            key='header key',
            value='header value',
        )
        
        APIMonitorQueryParam.objects.create(
            monitor=monitor,
            key='query key',
            value='query value',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        
        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].date, self.mock_current_time.date())
        self.assertEqual(result[0].hour, self.mock_current_time.hour)
        self.assertEqual(result[0].minute, self.mock_current_time.minute)
        self.assertEqual(result[0].success, True)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, '')
        
