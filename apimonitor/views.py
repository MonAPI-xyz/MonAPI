from datetime import datetime, timedelta
import pytz

from django.db.models import Avg, Count, Q
from django.utils import timezone
from django.conf import settings
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apimonitor.models import (APIMonitor, APIMonitorResult, APIMonitorQueryParam,
                               APIMonitorHeader, APIMonitorBodyForm, APIMonitorRawBody)
from apimonitor.serializers import (APIMonitorSerializer, APIMonitorListSerializer,
                                    APIMonitorQueryParamSerializer, APIMonitorHeaderSerializer,
                                    APIMonitorBodyFormSerializer, APIMonitorRawBodySerializer)


class APIMonitorViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):

    queryset = APIMonitor.objects.all()
    serializer_class = APIMonitorSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def create(self, request, *args, **kwargs):
        monitor_data = {
            'user': request.user,
            'name': request.data.get('name'),
            'method': request.data.get('method'),
            'url': request.data.get('url'),
            'schedule': request.data.get('schedule'),
            'body_type': request.data.get('body_type')
        }
        api_monitor_serializer = APIMonitorSerializer(data=monitor_data)
        if (api_monitor_serializer.is_valid()):
            monitor_obj = APIMonitor.objects.create(**monitor_data)
            error_log = []
            try:
                if request.data.get('query_params'):
                    for key_value_pair in request.data.get('query_params'):
                        if len(key_value_pair) == 2:
                            key, value = key_value_pair[0], key_value_pair[1]
                        else:
                            error_log += ["Please make sure you submit correct [query params]"]
                            break
                        record = {
                            'monitor': monitor_obj.id,
                            'key': key,
                            'value': value
                        }
                        if APIMonitorQueryParamSerializer(data=record).is_valid():
                            record['monitor'] = monitor_obj
                            APIMonitorQueryParam.objects.create(**record)
                        else:
                            error_log += ["Please make sure your [query params] key and value are valid strings!"]
                            break

                if request.data.get('headers'):
                    for key_value_pair in request.data.get('headers'):
                        if len(key_value_pair) == 2:
                            key, value = key_value_pair[0], key_value_pair[1]
                        else:
                            error_log += ["Please make sure you submit correct [headers]"]
                            break
                        record = {
                            'monitor': monitor_obj.id,
                            'key': key,
                            'value': value
                        }
                        if APIMonitorHeaderSerializer(data=record).is_valid():
                            record['monitor'] = monitor_obj
                            APIMonitorHeader.objects.create(**record)
                        else:
                            error_log += ["Please make sure your [headers] key and value are valid strings!"]
                            break


                if request.data.get('body_type') == 'FORM':
                    for key_value_pair in request.data.get('body_form'):
                        if len(key_value_pair) == 2:
                            key, value = key_value_pair[0], key_value_pair[1]
                        else:
                            error_log += ["Please make sure you submit correct [body form]"]
                            break
                        record = {
                            'monitor': monitor_obj.id,
                            'key': key,
                            'value': value
                        }
                        if APIMonitorBodyFormSerializer(data=record).is_valid():
                            record['monitor'] = monitor_obj
                            APIMonitorBodyForm.objects.create(**record)
                        else:
                            error_log += ["Please make sure your [body form] key and value are valid strings!"]
                            break
                elif request.data.get('body_type') == 'RAW':
                    record = {
                        'monitor': monitor_obj.id,
                        'body': request.data['raw_body']
                    }
                    if APIMonitorRawBodySerializer(data=record).is_valid():
                        record['monitor'] = monitor_obj
                        APIMonitorRawBody.objects.create(**record)
                    else:
                        error_log += ["Please make sure your [raw body] is a valid string or JSON!"]

                assert len(error_log) == 0, error_log
                serialized_obj = APIMonitorSerializer(monitor_obj)
                return Response(data=serialized_obj.data, status=status.HTTP_201_CREATED)
            except AssertionError as e:
                monitor_obj.delete()
                return Response(data={"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"error": "['Please make sure your [name, method, url, schedule, body_type] is valid']"}, status=status.HTTP_400_BAD_REQUEST)


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
            
            # Last result 
            last_result = APIMonitorResult.objects.filter(monitor=monitor).last()
            monitor.last_result = last_result
       
        serializer = APIMonitorListSerializer(queryset, many=True)
        return Response(serializer.data)
