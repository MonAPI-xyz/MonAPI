from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from alerts.serializers import AlertsConfigurationSerializer
from apimonitor.models import AlertsConfiguration

class AlertConfiguration(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):        
        config, _ = AlertsConfiguration.objects.get_or_create(team=request.auth.team)
        serializer = AlertsConfigurationSerializer(config)
        return Response(serializer.data)
    
    def post(self, request, format=None):        
        config, _ = AlertsConfiguration.objects.get_or_create(team=request.auth.team)
        serializer = AlertsConfigurationSerializer(config, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    