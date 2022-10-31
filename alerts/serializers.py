from rest_framework import serializers

from apimonitor.models import AlertsConfiguration
from alerts.models import ThresholdConfig

class AlertsConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertsConfiguration
        fields = [
            'is_slack_active',
            'slack_token',
            'slack_channel_id',
            'is_discord_active',
            'discord_bot_token',
            'discord_guild_id',
            'discord_channel_id',
            'is_pagerduty_active',
            'pagerduty_api_key',
            'pagerduty_default_from_email',
            'is_email_active',
            'email_host',
            'email_port',
            'email_username',
            'email_password',
            'email_use_tls',
            'email_use_ssl',
        ]

class ThresholdConfigSerialzier(serializers.ModelSerializer):
    class Meta:
        model = ThresholdConfig
        fields = [
            'user',
            'threshold_pct',
            'time_window',
        ]
