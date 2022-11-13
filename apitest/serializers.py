from rest_framework import serializers

from apimonitor.models import APIMonitor, APIMonitorQueryParam, APIMonitorHeader, APIMonitorRawBody, APIMonitorBodyForm, \
    APIMonitorResult, AssertionExcludeKey

class APITestQueryParamSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIMonitorQueryParam
        fields = [
            'key',
            'value',
        ]

class APITestHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIMonitorHeader
        fields = [
            'key',
            'value',
        ]

class APITestBodyFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIMonitorBodyForm
        fields = [
            'key',
            'value',
        ]

