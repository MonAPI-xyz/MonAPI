import pytz

from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.utils import timezone
from unittest.mock import patch
from django.test import TransactionTestCase
from io import StringIO

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from datetime import datetime
import time
import requests
import os

from apimonitor.models import APIMonitor, APIMonitorResult, AlertsConfiguration


class AlertsConfigurationTestCase(APITestCase):
    test_url = reverse('alert-configuration')
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

    def test_when_authenticated_and_dont_have_configuration_then_create_new_configuration(self):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        response = self.client.get(self.test_url, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "is_slack_active": False,
            "slack_token": "",
            "slack_channel_id": "",
            "is_discord_active": False,
            "discord_bot_token": "",
            "discord_guild_id": "",
            "discord_channel_id": "",
            "is_pagerduty_active": False,
            "pagerduty_api_key": "",
            "pagerduty_default_from_email": "",
            "pagerduty_service_id": "",
            "is_email_active": False,
            "email_host": "",
            "email_port": None,
            "email_username": "",
            "email_password": "",
            "email_use_tls": False,
            "email_use_ssl": False,
            'threshold_pct': 100,
            'time_window': '1H'
        })
        
        count = AlertsConfiguration.objects.count()
        self.assertEqual(count, 1)

    def test_when_authenticated_already_have_configuration_then_return_configuration(self):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        
        AlertsConfiguration.objects.create(
            user=user,
            is_slack_active=True,
            is_discord_active=True,
            is_pagerduty_active=True,
            is_email_active=True,
        )

        response = self.client.get(self.test_url, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "is_slack_active": True,
            "slack_token": "",
            "slack_channel_id": "",
            "is_discord_active": True,
            "discord_bot_token": "",
            "discord_guild_id": "",
            "discord_channel_id": "",
            "is_pagerduty_active": True,
            "pagerduty_api_key": "",
            "pagerduty_default_from_email": "",
            "pagerduty_service_id": "",
            "is_email_active": True,
            "email_host": "",
            "email_port": None,
            "email_username": "",
            "email_password": "",
            "email_use_tls": False,
            "email_use_ssl": False,
            'threshold_pct': 100,
            'time_window': '1H'
        })
    
    def test_when_authenticated_update_config_then_save_configuration(self):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        
        req_body = {
            "is_slack_active": True,
            "slack_token": "",
            "slack_channel_id": "",
            "is_discord_active": True,
            "discord_bot_token": "",
            "discord_guild_id": "",
            "discord_channel_id": "",
            "is_pagerduty_active": True,
            "pagerduty_api_key": "",
            "pagerduty_default_from_email": "",
            "pagerduty_service_id": "",
            "is_email_active": True,
            "email_host": "",
            "email_port": None,
            "email_username": "",
            "email_password": "",
            "email_use_tls": False,
            "email_use_ssl": False,
        }
        
        response = self.client.post(self.test_url, data=req_body, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "is_slack_active": True,
            "slack_token": "",
            "slack_channel_id": "",
            "is_discord_active": True,
            "discord_bot_token": "",
            "discord_guild_id": "",
            "discord_channel_id": "",
            "is_pagerduty_active": True,
            "pagerduty_api_key": "",
            "pagerduty_default_from_email": "",
            "pagerduty_service_id": "",
            "is_email_active": True,
            "email_host": "",
            "email_port": None,
            "email_username": "",
            "email_password": "",
            "email_use_tls": False,
            "email_use_ssl": False,
            'threshold_pct': 100,
            'time_window': '1H'
        })
        
        config = AlertsConfiguration.objects.get(user=user)
        self.assertEqual(config.is_slack_active, True)
        self.assertEqual(config.is_discord_active, True)
        self.assertEqual(config.is_pagerduty_active, True)
        self.assertEqual(config.is_email_active, True)
    
    def test_when_authenticated_update_config_invalid_data_then_return_bad_request(self):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        
        req_body = {
            "is_slack_active": None,
        }
        
        response = self.client.post(self.test_url, data=req_body, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"is_slack_active": ["This field may not be null."]})

class ThresholdConfigTest(APITestCase):
    test_url = reverse('alert-configuration')
    def test_threshold_config_can_be_created(self):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        req_body = {
            "is_slack_active": True,
            "slack_token": "",
            "slack_channel_id": "",
            "is_discord_active": True,
            "discord_bot_token": "",
            "discord_guild_id": "",
            "discord_channel_id": "",
            "is_pagerduty_active": True,
            "pagerduty_api_key": "",
            "pagerduty_default_from_email": "",
            "pagerduty_service_id": "",
            "is_email_active": True,
            "email_host": "",
            "email_port": None,
            "email_username": "",
            "email_password": "",
            "email_use_tls": False,
            "email_use_ssl": False,
            "threshold_pct": 95,
            "time_window": "6H"
        }

        response = self.client.post(self.test_url, data=req_body, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            "is_slack_active": True,
            "slack_token": "",
            "slack_channel_id": "",
            "is_discord_active": True,
            "discord_bot_token": "",
            "discord_guild_id": "",
            "discord_channel_id": "",
            "is_pagerduty_active": True,
            "pagerduty_api_key": "",
            "pagerduty_default_from_email": "",
            "pagerduty_service_id": "",
            "is_email_active": True,
            "email_host": "",
            "email_port": None,
            "email_username": "",
            "email_password": "",
            "email_use_tls": False,
            "email_use_ssl": False,
            "threshold_pct": 95,
            "time_window": "6H"
        })

        config = AlertsConfiguration.objects.get(user=user)
        self.assertEqual(config.is_slack_active, True)
        self.assertEqual(config.is_discord_active, True)
        self.assertEqual(config.is_pagerduty_active, True)
        self.assertEqual(config.is_email_active, True)

    def test_threshold_pct_cannot_be_negative_and_time_window_must_be_valid(self):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        req_body = {
            "is_slack_active": True,
            "slack_token": "",
            "slack_channel_id": "",
            "is_discord_active": True,
            "discord_bot_token": "",
            "discord_guild_id": "",
            "discord_channel_id": "",
            "is_pagerduty_active": True,
            "pagerduty_api_key": "",
            "pagerduty_default_from_email": "",
            "pagerduty_service_id": "",
            "is_email_active": True,
            "email_host": "",
            "email_port": None,
            "email_username": "",
            "email_password": "",
            "email_use_tls": False,
            "email_use_ssl": False,
            "threshold_pct": -1,
            "time_window": "0H"
        }

        response = self.client.post(self.test_url, data=req_body, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['threshold_pct'][0].title(), "Ensure This Value Is Greater Than Or Equal To 1.")
        self.assertEqual(response.data['time_window'][0].title(), '"0H" Is Not A Valid Choice.')

    def test_threshold_pct_cannot_be_larger_than_100(self):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        token = Token.objects.create(user=user)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        req_body = {
            "is_slack_active": True,
            "slack_token": "",
            "slack_channel_id": "",
            "is_discord_active": True,
            "discord_bot_token": "",
            "discord_guild_id": "",
            "discord_channel_id": "",
            "is_pagerduty_active": True,
            "pagerduty_api_key": "",
            "pagerduty_default_from_email": "",
            "pagerduty_service_id": "",
            "is_email_active": True,
            "email_host": "",
            "email_port": None,
            "email_username": "",
            "email_password": "",
            "email_use_tls": False,
            "email_use_ssl": False,
            "threshold_pct": 101,
            "time_window": "1H"
        }

        response = self.client.post(self.test_url, data=req_body, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['threshold_pct'][0].title(), "Ensure This Value Is Less Than Or Equal To 100.")

class CronAlertsManagementCommand(TransactionTestCase):
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    mock_current_time = local_timezone.localize(datetime(2022,9,20,10))
    
    def setUp(self):
        # Mock time function
        timezone.now = lambda: self.mock_current_time
        timezone.localtime = lambda: self.mock_current_time
        os.environ['CRON_INTERVAL_IN_SECONDS'] = '2'
    
    def call_command(self, *args, **kwargs):
        out = StringIO()
        call_command("run_cron_alerts", *args, stdout=out, stderr=StringIO(), **kwargs)
        return out.getvalue()
    
    # Mock interrupt
    @patch("alerts.management.commands.run_cron_alerts.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.post")
    def test_when_api_monitor_result_empty_then_not_send_alert(self, mock_request, mock_interrupt):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='EMPTY',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)
        
        self.assertFalse(mock_request.called)
        
    @patch("time.sleep", side_effect=InterruptedError)
    @patch("requests.post")
    def test_when_mock_time_sleep_then_interrupt_on_sleep(self, mock_request, *args):
        try:
            self.call_command()
        except InterruptedError:
            pass
        
        self.assertFalse(mock_request.called)
        
    @patch("alerts.management.commands.run_cron_alerts.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.post")
    def test_when_env_config_invalid_then_use_default(self, mock_request, mock_interrupt):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        os.environ['CRON_ALERTS_THREAD_COUNT'] = 'invalid int'
        
        monitor = APIMonitor.objects.create(
            user=user,
            name='apimonitor',
            method='GET',
            url='https://monapi.xyz',
            schedule='60MIN',
            body_type='EMPTY',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)
        
        self.assertFalse(mock_request.called)
        
    @patch("alerts.management.commands.run_cron_alerts.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.post")
    def test_when_api_monitor_failed_but_notification_disabled_then_not_send_alert(self, mock_request, mock_interrupt):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        AlertsConfiguration.objects.create(
            user=user,
        )
        
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
            success=False,
            status_code=500,
            log_response='resp',
            log_error='error',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)
        self.assertFalse(mock_request.called)
        
    @patch("alerts.management.commands.run_cron_alerts.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.post")
    def test_when_api_monitor_failed_and_pagerduty_enabled_then_send_alert(self, mock_request, mock_interrupt):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        AlertsConfiguration.objects.create(
            user=user,
            is_pagerduty_active=True,
        )
        
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
            success=False,
            status_code=500,
            log_response='resp',
            log_error='error',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)
        
        args = mock_request.call_args.args
        self.assertEqual(args[0], 'https://api.pagerduty.com/incidents')
        
    @patch("alerts.management.commands.run_cron_alerts.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.post")
    def test_when_api_monitor_failed_and_pagerduty_error_then_do_nothing(self, mock_request, mock_interrupt):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        AlertsConfiguration.objects.create(
            user=user,
            is_pagerduty_active=True,
        )
        
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
            success=False,
            status_code=500,
            log_response='resp',
            log_error='error',
        )
        
        mock_request.side_effect = Exception()
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)
        
        args = mock_request.call_args.args
        self.assertEqual(args[0], 'https://api.pagerduty.com/incidents')
         
    @patch("alerts.management.commands.run_cron_alerts.mock_cron_interrupt", side_effect = [None, InterruptedError])
    @patch("requests.post")
    def test_when_api_monitor_failed_and_last_notified_within_5min_then_not_send_alert(self, mock_request, mock_interrupt):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        AlertsConfiguration.objects.create(
            user=user,
            is_pagerduty_active=True,
        )
        
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
            success=False,
            status_code=500,
            log_response='resp',
            log_error='error',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)
        
        self.assertEqual(mock_request.call_count, 1)
        
    @patch("alerts.management.commands.run_cron_alerts.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.post")
    def test_when_api_monitor_failed_and_discord_enabled_then_send_alert(self, mock_request, mock_interrupt):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        AlertsConfiguration.objects.create(
            user=user,
            is_discord_active=True,
        )
        
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
            success=False,
            status_code=500,
            log_response='resp',
            log_error='error',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)
        
        self.assertFalse(mock_request.called)
        
    @patch("alerts.management.commands.run_cron_alerts.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.post")
    def test_when_api_monitor_failed_and_email_enabled_then_send_alert(self, mock_request, mock_interrupt):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        AlertsConfiguration.objects.create(
            user=user,
            is_email_active=True,
        )
        
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
            success=False,
            status_code=500,
            log_response='resp',
            log_error='error',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)
        
        self.assertFalse(mock_request.called)
    @patch("alerts.management.commands.run_cron_alerts.mock_cron_interrupt", side_effect = [None, InterruptedError])
    @patch("requests.post")
    def test_when_api_monitor_failed_and_last_notified_within_5min_then_not_send_alert_slack(self, mock_request, mock_interrupt):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        AlertsConfiguration.objects.create(
            user=user,
            is_slack_active=True,
        )
        
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
            success=False,
            status_code=500,
            log_response='resp',
            log_error='error',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)
        
        self.assertEqual(mock_request.call_count, 1)


    @patch("alerts.management.commands.run_cron_alerts.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.post")
    def test_when_api_monitor_success_and_slack_enabled_then_not_send_alert(self, mock_request, mock_interrupt):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        AlertsConfiguration.objects.create(
            user=user,
            is_slack_active=True,
        )
        
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
            log_error='',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)
        self.assertFalse(mock_request.called)

    @patch("alerts.management.commands.run_cron_alerts.mock_cron_interrupt", side_effect=InterruptedError)
    @patch("requests.post")
    def test_when_api_monitor_failed_and_slack_enabled_then_send_alert(self, mock_request, mock_interrupt):
        user = User.objects.create_user(username='test', email='test@test.com', password='test123')
        AlertsConfiguration.objects.create(
            user=user,
            is_slack_active=True,
        )
        
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
            success=False,
            status_code=500,
            log_response='resp',
            log_error='error',
        )
        
        try:
            self.call_command()
        except InterruptedError:
            pass
        time.sleep(0.1)
        args = mock_request.call_args.args
        self.assertEqual(args[0], 'https://slack.com/api/chat.postMessage')
        
    