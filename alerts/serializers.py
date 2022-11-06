from rest_framework import serializers

from apimonitor.models import AlertsConfiguration

class AlertsConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertsConfiguration
        fields = [
            'is_slack_active',
            'slack_token',
            'slack_channel_id',
            'is_discord_active',
            'discord_webhook_url',
            'is_pagerduty_active',
            'pagerduty_api_key',
            'pagerduty_default_from_email',
            'pagerduty_service_id',
            'is_email_active',
            'email_name',
            'email_address',
            'email_host',
            'email_port',
            'email_username',
            'email_password',
            'email_use_tls',
            'email_use_ssl',
            'threshold_pct',
            'time_window',
        ]
