from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from apimonitor.models import APIMonitorResult
from error_logs.serializers import ErrorLogsSerializer

class ErrorLogsViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):

  queryset = APIMonitorResult.objects.all()
  serializer_class = ErrorLogsSerializer
  permission_classes = [IsAuthenticated]
  
  def get_queryset(self):
    queryset = APIMonitorResult.objects.filter(monitor__user=self.request.user, success=False)
    return queryset