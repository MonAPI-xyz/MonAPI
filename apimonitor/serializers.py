from rest_framework import serializers

from apimonitor.models import APIMonitor, APIMonitorQueryParam, APIMonitorHeader, APIMonitorRawBody, \
    APIMonitorResult, AssertionExcludeKey

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



class AssertionExcludeKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssertionExcludeKey
        fields = [
            'id',
            'monitor',
            'exclude_key',
        ]


class APIMonitorDetailSuccessRateSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    success = serializers.IntegerField()
    failed = serializers.IntegerField()


class APIMonitorDetailResponseTimeSerializer(serializers.Serializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    avg = serializers.IntegerField()


class APIMonitorSerializer(serializers.ModelSerializer):
    query_params = APIMonitorQueryParamSerializer(many=True, required=False, allow_null=True)
    headers = APIMonitorHeaderSerializer(many=True, required=False, allow_null=True)
    body_form = APIMonitorBodyFormSerializer(many=True, required=False, allow_null=True)
    raw_body = APIMonitorRawBodySerializer(required=False, allow_null=True)
    previous_step_id = serializers.PrimaryKeyRelatedField(read_only=True, many=False)
    exclude_keys = AssertionExcludeKeySerializer(many=True, required=False, allow_null=True)
    
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
            'previous_step_id',
            'assertion_type',
            'assertion_value',
            'is_assert_json_schema_only',
            'exclude_keys',
        ]


class APIMonitorResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIMonitorResult
        fields = [
            'id',
            'monitor',
            'execution_time',
            'response_time',
            'success',
            'status_code',
            'log_response',
            'log_error',
        ]


class APIMonitorListSerializer(APIMonitorSerializer):
    success_rate = serializers.DecimalField(None, decimal_places=1)
    avg_response_time = serializers.IntegerField()
    success_rate_history = APIMonitorDetailSuccessRateSerializer(many=True)
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

class APIMonitorDashboardSerializer(serializers.Serializer):
    success_rate = APIMonitorDetailSuccessRateSerializer(many=True)
    response_time = APIMonitorDetailResponseTimeSerializer(many=True)


class APIMonitorRetrieveSerializer(APIMonitorSerializer):
    success_rate = APIMonitorDetailSuccessRateSerializer(many=True)
    response_time = APIMonitorDetailResponseTimeSerializer(many=True)

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
            'previous_step_id',
            'success_rate',
            'response_time',
            'assertion_type',
            'assertion_value',
            'is_assert_json_schema_only',
            'exclude_keys',
        ]
