from rest_framework import serializers

from apimonitor.models import APIMonitor


class APIMonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIMonitor
        fields = [
            'id',
            'name',
            'method',
            'url',
            'schedule',
            'body_type',
            'query_params',
            'headers',
            'body_form',
            'raw_body',
        ]
