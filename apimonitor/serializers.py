from rest_framework import serializers

from apimonitor.models import APIMonitor, APIMonitorQueryParam, APIMonitorHeader, APIMonitorBodyForm, APIMonitorRawBody, APIMonitorResult


class APIMonitorQueryParamSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIMonitorQueryParam
        fields = [
            'id',
            'monitor',
            'key',
            'value',
        ]
        
        
class APIMonitorHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIMonitorHeader
        fields = [
            'id',
            'monitor',
            'key',
            'value',
        ]


class APIMonitorBodyFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIMonitorHeader
        fields = [
            'id',
            'monitor',
            'key',
            'value',
        ]


class APIMonitorRawBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIMonitorRawBody
        fields = [
            'id',
            'monitor',
            'body',
        ]


class APIMonitorSuccessRateHistorySerializer(serializers.Serializer):
    date = serializers.DateField()
    hour = serializers.IntegerField()
    minute = serializers.IntegerField()
    success = serializers.IntegerField()
    failed = serializers.IntegerField()
    

class APIMonitorSerializer(serializers.ModelSerializer):
    query_params = APIMonitorQueryParamSerializer(many=True)
    headers = APIMonitorHeaderSerializer(many=True)
    body_form = APIMonitorBodyFormSerializer(many=True)
    raw_body = APIMonitorRawBodySerializer()
    
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
        
        
class APIMonitorResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIMonitorResult
        fields = [
            'id',
            'monitor',
            'execution_time',
            'date',
            'hour',
            'minute',
            'response_time',
            'success',
            'log_response',
        ]


class APIMonitorListSerializer(APIMonitorSerializer):
    success_rate = serializers.DecimalField(None, decimal_places=1)
    avg_response_time = serializers.IntegerField()
    success_rate_history = APIMonitorSuccessRateHistorySerializer(many=True)
    last_result = APIMonitorResultSerializer()
    
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
            'success_rate',
            'avg_response_time',
            'success_rate_history',
            'last_result',
        ]
