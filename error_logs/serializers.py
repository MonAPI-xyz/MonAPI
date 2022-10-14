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
          'response_time',
          'success',
          'status_code',
          'log_response',
          'log_error',
      ]