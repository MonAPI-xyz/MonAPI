from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from apimonitor.models import APIMonitor
from apimonitor.serializers import APIMonitorSerializer


class APIMonitorViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = APIMonitor.objects.all()
    serializer_class = APIMonitorSerializer
    