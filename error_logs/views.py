from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apimonitor.models import APIMonitorResult
from error_logs.serializers import ErrorLogsSerializer

class ErrorLogsViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):

  queryset = APIMonitorResult.objects.all()
  serializer_class = ErrorLogsSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    limit = 1500
    queryset = APIMonitorResult.objects.filter(monitor__user=self.request.user, success=False)\
      .order_by("-execution_time").select_related('monitor')[:limit]
    return queryset
  
  def retrieve(self, request, pk=None):
    queryset = APIMonitorResult.objects.filter(monitor__user=self.request.user, success=False)\
      .select_related('monitor')
      
    obj = get_object_or_404(queryset, id=pk)
    serializer = self.get_serializer(obj)
    return Response(serializer.data)

