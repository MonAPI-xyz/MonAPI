import pytz

from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from datetime import datetime

from apimonitor.models import AlertsConfiguration


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