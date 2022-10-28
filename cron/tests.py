import os
from django.test import TestCase, TransactionTestCase
from django.conf import settings
from django.utils import timezone
from django.core.management import call_command
from django.contrib.auth.models import User
from unittest.mock import patch
from io import StringIO
from datetime import datetime
import pytz
import requests
import time

from apimonitor.models import APIMonitor, APIMonitorBodyForm, APIMonitorHeader, APIMonitorQueryParam, APIMonitorRawBody, APIMonitorResult, AssertionExcludeKey
from cron.management.commands.run_cron import Command


class MockResponse:
    def __init__(self, response, status_code):
        self.status_code = status_code
        self.content = response.encode('utf-8')


def mocked_request_get(*args, **kwargs):
    if args[0] == 'https://monapitestprev.xyz':
        return MockResponse('{"testing": "testing value"}', 200)
    elif args[0] == 'https://mockerrorstatuscode.xyz':
        return MockResponse('{"testing": "testing value"}', 400)
    elif args[0] == 'https://monapinonjson.xyz':
        return MockResponse('NonJSON response', 200)
    elif args[0] == 'https://mockiterable.xyz':
        return MockResponse('{"key": [{"key":"value"}], "key2":[]}', 200)
    return MockResponse("{\"key\": \"value\"}", 200)

def mocked_request_get_sleep(*args, **kwargs):
    time.sleep(3)
    return MockResponse("{\"key\": \"value\"}", 200)


def mocked_request_get_exception(*args, **kwargs):
    raise requests.exceptions.Timeout("Request timed out.")

class CronAccessDictWithKey(TestCase):
    def test_when_key_exists_then_replace_string(self):
        command = Command()
        res = command.replace_string_with_json_result("Token {{test}}", {"test": "value"})
        self.assertEqual(res, "Token value")
        
    def test_when_key_not_exists_then_raise_key_error(self):
        command = Command()
        with self.assertRaises(KeyError) as context:
            res = command.replace_string_with_json_result("Token {{not_exists_key}}", {"test": "value"})
        
        self.assertTrue('Value not found while accessing with key "not_exists_key"' in str(context.exception))
        
    def test_when_key_using_array_index_then_replace_with_value(self):
        command = Command()
        res = command.replace_string_with_json_result("Token {{testarray[0]}}", {"testarray": ["value"]})
        self.assertEqual(res, "Token value")
        
    def test_when_nested_array_key_not_exists_then_raise_key_error(self):
        command = Command()
        with self.assertRaises(KeyError) as context:
            res = command.replace_string_with_json_result("Token {{testarray.testarray3[0]}}", {"testarray": {"testarray2": ["value"]}})
            
        self.assertTrue('Value not found while accessing with key "testarray.testarray3[0]"' in str(context.exception))
        
    def test_when_nested_array_not_list_type_then_raise_key_error(self):
        command = Command()
        with self.assertRaises(KeyError) as context:
            res = command.replace_string_with_json_result("Token {{testarray.testarray2[0]}}", {"testarray": {"testarray2": "value"}})
            
        self.assertTrue('Value not found while accessing with key "testarray.testarray2[0]"' in str(context.exception))
        
    def test_when_nested_array_index_out_of_range_then_raise_key_error(self):
        command = Command()
        with self.assertRaises(KeyError) as context:
            res = command.replace_string_with_json_result("Token {{testarray.testarray2[1]}}", {"testarray": {"testarray2": ["value"]}})
            
        self.assertTrue('Value not found while accessing with key "testarray.testarray2[1]"' in str(context.exception))
        
    def test_when_nested_not_found_then_raise_key_error(self):
        command = Command()
        with self.assertRaises(KeyError) as context:
            res = command.replace_string_with_json_result("Token {{testarray.testarray2[0].testarray3}}", {"testarray": {"testarray2": ["value"]}})
            
        self.assertTrue('Value not found while accessing with key "testarray.testarray2[0].testarray3"' in str(context.exception))


class CronManagementCommand(TransactionTestCase):
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    mock_current_time = local_timezone.localize(datetime(2022,9,20,10))
    
    def setUp(self):
        # Mock time function
        timezone.now = lambda: self.mock_current_time
        timezone.localtime = lambda: self.mock_current_time
    
    def call_command(self, *args, **kwargs):
        out = StringIO()
        call_command("run_cron", *args, stdout=out, stderr=StringIO(), **kwargs)
        return out.getvalue()
    
    # Mock interrupt
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
    def test_when_not_exists_api_monitor_then_no_change(self, *args):
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)
        
        result = APIMonitorResult.objects.count()
        self.assertEqual(result, 0)
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
    def test_when_thread_environment_config_invalid_then_use_default(self, *args):
        os.environ['CRON_THREAD_COUNT'] = 'invalid type'
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)
        
        result = APIMonitorResult.objects.count()
        self.assertEqual(result, 0)
        del os.environ['CRON_THREAD_COUNT']
        
    @patch("time.sleep", side_effect=InterruptedError)
    def test_when_mock_time_sleep_then_interrupt_on_sleep(self, *args):
        try:
            self.call_command()
        except InterruptedError:
            pass

        result = APIMonitorResult.objects.count()
        self.assertEqual(result, 0)
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
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
            response_time=10,
            success=True,
            status_code=200,
            log_response='resp',
            log_error='error',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)

        count = APIMonitorResult.objects.count()
        self.assertEqual(count, 1)
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
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
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, True)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, '')
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt")
    @patch("requests.get", mocked_request_get_sleep)
    def test_when_result_not_exists_in_given_interval_and_checked_twice_then_run_only_once(self, mock_cron, *args):
        mock_cron.side_effect = [None, InterruptedError]
        
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
        
        time.sleep(4)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, True)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, '')
        
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
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
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, True)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, '')
        
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
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
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, True)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, '')
        
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
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
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, True)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, '')
        
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
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
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, False)
        self.assertEqual(result[0].log_response, "")
        self.assertEqual(result[0].log_error, 'Request timed out.')
        
           
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
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
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, True)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, '')
        
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
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
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, True)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, '')
        
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
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
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, True)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, '')
        
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
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
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, True)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, '')
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.delete", mocked_request_get)
    def test_when_status_code_not_2xx_then_test_success_false(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='DELETE',
            url='https://mockerrorstatuscode.xyz',
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
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, False)
        self.assertEqual(result[0].log_response, "{\"testing\": \"testing value\"}")
        self.assertEqual(result[0].log_error, 'Error code not in acceptable range 2xx')
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.get", mocked_request_get)
    def test_when_api_monitor_with_previous_step_then_run_previous_step_first(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        monitor_prev = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapitestprev.xyz',
            schedule='60MIN',
            body_type='RAW',
        )
        
        APIMonitorResult.objects.create(
            monitor=monitor_prev,
            execution_time=self.mock_current_time,
            response_time=10,
            success=True,
            status_code=200,
            log_response='resp',
            log_error='error',
        )
        
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='RAW',
            previous_step=monitor_prev,
        )
        
        APIMonitorHeader.objects.create(
            monitor=monitor,
            key='header key',
            value='header value',
        )
        
        APIMonitorQueryParam.objects.create(
            monitor=monitor,
            key='query key',
            value='{{testing}}',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1].success, True)
        self.assertEqual(result[1].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[1].log_error, '')
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.get", mocked_request_get)
    def test_when_api_monitor_with_previous_step_over_10_monitor_then_return_error(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        monitor_prev = None
        for i in range(11):
            monitor_prev = APIMonitor.objects.create(
                user=user,
                name='apimonitor',
                method='GET',
                url='https://monapitestprev.xyz',
                schedule='60MIN',
                body_type='RAW',
                previous_step=monitor_prev,
            )
            
            APIMonitorResult.objects.create(
                monitor=monitor_prev,
                execution_time=self.mock_current_time,
                response_time=10,
                success=True,
                status_code=200,
                log_response='resp',
                log_error='error',
            )
        
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='RAW',
            previous_step=monitor_prev,
        )
        
        APIMonitorHeader.objects.create(
            monitor=monitor,
            key='header key',
            value='header value',
        )
        
        APIMonitorQueryParam.objects.create(
            monitor=monitor,
            key='query key',
            value='{{testing}}',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 12)
        self.assertEqual(result[11].success, False)
        self.assertEqual(result[11].log_response, "")
        self.assertIn('Depth limit of previous step API monitor reached (maximum: 10)', result[11].log_error)
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.get", mocked_request_get)
    def test_when_api_monitor_with_recursion_then_return_error(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        monitor_prev = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapitestprev.xyz',
            schedule='60MIN',
            body_type='RAW',
        )
        
        APIMonitorResult.objects.create(
            monitor=monitor_prev,
            execution_time=self.mock_current_time,
            response_time=10,
            success=True,
            status_code=200,
            log_response='resp',
            log_error='error',
        )
        
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='RAW',
            previous_step=monitor_prev,
        )
        
        monitor_prev.previous_step = monitor
        monitor_prev.save()
        
        APIMonitorHeader.objects.create(
            monitor=monitor,
            key='header key',
            value='header value',
        )
        
        APIMonitorQueryParam.objects.create(
            monitor=monitor,
            key='query key',
            value='{{testing}}',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1].success, False)
        self.assertEqual(result[1].log_response, "")
        self.assertIn('Request aborted due to recursion of API monitor steps', result[1].log_error)
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.get", mocked_request_get)
    def test_when_api_monitor_key_not_exists_then_return_error(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        monitor_prev = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapitestprev.xyz',
            schedule='60MIN',
            body_type='RAW',
        )
        
        APIMonitorResult.objects.create(
            monitor=monitor_prev,
            execution_time=self.mock_current_time,
            response_time=10,
            success=True,
            status_code=200,
            log_response='resp',
            log_error='error',
        )
        
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='RAW',
            previous_step=monitor_prev,
        )
        
        APIMonitorHeader.objects.create(
            monitor=monitor,
            key='header key',
            value='header value',
        )
        
        APIMonitorQueryParam.objects.create(
            monitor=monitor,
            key='query key',
            value='{{testing.testing}}',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1].success, False)
        self.assertEqual(result[1].log_response, "{\"testing\": \"testing value\"}")
        self.assertIn('Error while preparing API monitor params: \'Value not found while accessing with key "testing.testing"\'', result[1].log_error)
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.get", mocked_request_get)
    def test_when_api_monitor_return_non_json_then_return_success(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        
        monitor_prev = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapinonjson.xyz',
            schedule='60MIN',
            body_type='RAW',
        )
        
        APIMonitorResult.objects.create(
            monitor=monitor_prev,
            execution_time=self.mock_current_time,
            response_time=10,
            success=True,
            status_code=200,
            log_response='resp',
            log_error='error',
        )
        
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapinonjson.xyz',
            schedule='60MIN',
            body_type='RAW',
            previous_step=monitor_prev,
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
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1].success, True)
        self.assertEqual(result[1].log_response, "NonJSON response")
        self.assertEqual(result[1].log_error, '')
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.get", mocked_request_get)
    def test_when_api_monitor_assert_text_failure_then_error(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapinonjson.xyz',
            schedule='60MIN',
            body_type='RAW',
            assertion_type='TEXT',
            assertion_value='',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, False)
        self.assertEqual(result[0].log_response, "NonJSON response")
        self.assertEqual(result[0].log_error, 'Assertion text failed.\nExpected: ""\nGot: "NonJSON response"')
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.get", mocked_request_get)
    def test_when_api_monitor_assert_json_invalid_response_then_error(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapinonjson.xyz',
            schedule='60MIN',
            body_type='RAW',
            assertion_type='JSON',
            assertion_value='{\"key\": \"value\"}',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, False)
        self.assertEqual(result[0].log_response, "NonJSON response")
        self.assertEqual(result[0].log_error, 'Failed to decode JSON api response')
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.get", mocked_request_get)
    def test_when_api_monitor_assert_json_invalid_assert_value_then_error(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='RAW',
            assertion_type='JSON',
            assertion_value='Invalid JSON',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, False)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, 'Failed to decode JSON monitor assertions value')
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.get", mocked_request_get)
    def test_when_api_monitor_assert_json_different_value_then_error(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='RAW',
            assertion_type='JSON',
            assertion_value='{\"key\": \"value2\"}',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, False)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, 'Different value detected on root[\'key\'], expected "value2" but found "value"')
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.get", mocked_request_get)
    def test_when_api_monitor_assert_json_key_only_then_success(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='RAW',
            assertion_type='JSON',
            assertion_value='{\"key\": \"value2\"}',
            is_assert_json_schema_only=True,
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, True)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, '')
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.get", mocked_request_get)
    def test_when_api_monitor_assert_json_exclude_keys_then_success(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='RAW',
            assertion_type='JSON',
            assertion_value='{\"key\": \"value2\"}',
        )
        
        AssertionExcludeKey.objects.create(
            monitor=monitor,
            exclude_key='key',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, True)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, '')
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.get", mocked_request_get)
    def test_when_api_monitor_assert_json_different_type_then_error(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='RAW',
            assertion_type='JSON',
            assertion_value='{\"key\": 1}',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, False)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, 'Different type detected on root[\'key\'], expected "1" (<class \'int\'>) but found "value" (<class \'str\'>)')
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.get", mocked_request_get)
    def test_when_api_monitor_assert_json_dict_add_remove_then_error(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='RAW',
            assertion_type='JSON',
            assertion_value='{"key2": "value"}',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, False)
        self.assertEqual(result[0].log_response, "{\"key\": \"value\"}")
        self.assertEqual(result[0].log_error, 'New key detected with keys [root[\'key\']]\nMissing key detected with keys [root[\'key2\']]')
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.get", mocked_request_get)
    def test_when_api_monitor_assert_json_iterable_add_remove_then_error(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://mockiterable.xyz',
            schedule='60MIN',
            body_type='RAW',
            assertion_type='JSON',
            assertion_value='{"key":[] , "key2":[{"key":"value"}]}',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, False)
        self.assertEqual(result[0].log_response, '{"key": [{"key":"value"}], "key2":[]}')
        self.assertEqual(result[0].log_error, 'Found iterable item added with keys dict_keys(["root[\'key\'][0]"])\nFound iterable item removed with keys dict_keys(["root[\'key2\'][0]"])')
        
        
    @patch("cron.management.commands.run_cron.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.get", mocked_request_get)
    def test_when_api_monitor_assert_json_iterable_exclude_then_success(self, *args):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://mockiterable.xyz',
            schedule='60MIN',
            body_type='RAW',
            assertion_type='JSON',
            assertion_value='{"key":[] , "key2":[{"key":"value"}]}',
        )
        
        AssertionExcludeKey.objects.create(
            monitor=monitor,
            exclude_key='key[0]',
        )
        
        AssertionExcludeKey.objects.create(
            monitor=monitor,
            exclude_key='key2[0]',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)

        result = APIMonitorResult.objects.all()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].success, True)
        self.assertEqual(result[0].log_response, '{"key": [{"key":"value"}], "key2":[]}')
        self.assertEqual(result[0].log_error, '')
        
        
