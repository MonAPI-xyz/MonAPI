from rest_framework import serializers

from apimonitor.models import APIMonitorResult
from apimonitor.serializers import APIMonitorSerializer

class ErrorLogsSerializer(serializers.ModelSerializer):
  monitor = APIMonitorSerializer()
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
          'log_error',
      ]