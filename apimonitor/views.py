from datetime import datetime, timedelta
import pytz

from django.db.models import Avg, Count, Q
from django.utils import timezone
from django.conf import settings
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apimonitor.models import APIMonitor, APIMonitorResult
from apimonitor.serializers import APIMonitorSerializer, APIMonitorRetrieveSerializer


class APIMonitorViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = APIMonitor.objects.all()
    serializer_class = APIMonitorSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        queryset = APIMonitor.objects.filter(user=self.request.user)
        return queryset
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Truncate last 24 hours until hour
        local_timezone = pytz.timezone(settings.TIME_ZONE)
        last_24_hour = timezone.now() - timedelta(days=1)
        last_24_hour = last_24_hour.replace(hour=last_24_hour.hour + 1, minute=0, second=0, microsecond=0)
            
        # Append summary to each monitor
        for monitor in queryset:
            # Average response time
            avg_response_time = APIMonitorResult.objects \
                .filter(monitor=monitor, execution_time__gte=last_24_hour) \
                .aggregate(avg=Avg('response_time'))
            monitor.avg_response_time = avg_response_time['avg']
            
            if monitor.avg_response_time == None:
                monitor.avg_response_time = 0
            
            # Average success rate
            success_count = APIMonitorResult.objects \
                .filter(monitor=monitor, execution_time__gte=last_24_hour) \
                .aggregate(
                    s=Count('success', filter=Q(success=True)), 
                    f=Count('success', filter=Q(success=False)),
                    total=Count('pk'),
                )
            
            if success_count['total'] == 0:
                monitor.success_rate = 100
            else:
                monitor.success_rate = success_count['s'] / (success_count['s'] + success_count['f']) * 100
            
            # Success rate history
            success_rate_per_hour = APIMonitorResult.objects \
                .filter(monitor=monitor, execution_time__gte=last_24_hour) \
                .values('date', 'hour') \
                .annotate(
                    s=Count('success', filter=Q(success=True)), 
                    f=Count('success', filter=Q(success=False)),
                ) \
                .order_by('date', 'hour')
                
            # Convert query result to dictionary based on datetime
            success_rate_history_dict = {}
            for sc_per_hour in success_rate_per_hour:
                date_time_sc = local_timezone.localize(datetime(
                    sc_per_hour['date'].year, 
                    sc_per_hour['date'].month, 
                    sc_per_hour['date'].day, 
                    sc_per_hour['hour']
                ))
                success_rate_history_dict[date_time_sc.isoformat()] = {
                    'date': sc_per_hour['date'],
                    'hour': sc_per_hour['hour'],
                    'minute': 0,
                    'success': sc_per_hour['s'],
                    'failed': sc_per_hour['f'],
                }
            
            success_rate_history = []
            date_time_sc = last_24_hour
            for _ in range(24):
                date_time_sc_in_zone = date_time_sc.astimezone()
                
                if date_time_sc_in_zone.isoformat() in success_rate_history_dict:
                    success_rate_history.append(success_rate_history_dict[date_time_sc_in_zone.isoformat()])
                else:
                    success_rate_history.append({
                        'date': date_time_sc_in_zone.date(),
                        'hour': date_time_sc_in_zone.hour,
                        'minute': 0,
                        'success': 0,
                        'failed': 0,
                    })
                date_time_sc += timedelta(hours=1)
           
            monitor.success_rate_history = success_rate_history
        
        serializer = APIMonitorRetrieveSerializer(queryset, many=True)
        return Response(serializer.data)