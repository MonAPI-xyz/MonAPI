from rest_framework import serializers

from apimonitor.models import APIMonitorResult, APIMonitor

class ErrorLogsAPIMonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIMonitor
        fields = [
            'id',
            'name',
            'method',
            'url',
            'schedule',
            'body_type',
            'previous_step_id',
            'assertion_type',
            'assertion_value',
            'is_assert_json_schema_only',
        ]


class ErrorLogsSerializer(serializers.ModelSerializer):
  monitor = ErrorLogsAPIMonitorSerializer()
  
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