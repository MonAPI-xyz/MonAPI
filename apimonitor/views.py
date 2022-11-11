from datetime import timedelta

from django.db.models import Avg, Count, Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from utils import try_parse_int
import json

from apimonitor.models import (APIMonitor, APIMonitorResult, APIMonitorQueryParam,
                               APIMonitorHeader, APIMonitorBodyForm, APIMonitorRawBody, AssertionExcludeKey)
from apimonitor.serializers import (APIMonitorSerializer, APIMonitorListSerializer,
                                    APIMonitorQueryParamSerializer, APIMonitorHeaderSerializer,
                                    APIMonitorBodyFormSerializer, APIMonitorRawBodySerializer,
                                    APIMonitorRetrieveSerializer, APIMonitorDashboardSerializer,
                                    AssertionExcludeKeySerializer, APIMonitorDetailSuccessRateSerializer, 
                                    APIMonitorDetailResponseTimeSerializer)

from monapi.cache import (CACHE_KEY_API_MONITOR_LIST, CACHE_KEY_API_MONITOR_DETAIL_STATS, 
                          CACHE_KEY_API_MONITOR_STATS, get_cache_value, set_cache_value)


class APIMonitorViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.CreateModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):

    queryset = APIMonitor.objects.all()
    serializer_class = APIMonitorSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"
    
    def get_queryset(self):
        if self.action == 'list':
            return APIMonitor.objects.filter(user=self.request.user)    
        
        return APIMonitor.objects.filter(user=self.request.user) \
            .prefetch_related('query_params', 'headers', 'body_form', 'raw_body', 'exclude_keys')
    
    def get_monitor_data_from_request(self, request):
        monitor_data = {
            'user': request.user,
            'name': request.data.get('name'),
            'method': request.data.get('method'),
            'url': request.data.get('url'),
            'schedule': request.data.get('schedule'),
            'body_type': request.data.get('body_type'),
            'previous_step_id': None if request.data.get('previous_step_id') == '' else request.data.get('previous_step_id', None),
            'assertion_type': request.data.get('assertion_type', "DISABLED"),
            'assertion_value': request.data.get('assertion_value', ""),
            'is_assert_json_schema_only': request.data.get('is_assert_json_schema_only', False)
        }
        return monitor_data

    def update(self, request, *args, **kwargs):
        monitor_data = self.get_monitor_data_from_request(request)

        if monitor_data['previous_step_id'] is not None:
            if try_parse_int(monitor_data['previous_step_id']):
                monitor_data['previous_step_obj'] = APIMonitor.objects.get(pk=int(monitor_data['previous_step_id']))
            else:
                return Response(data={"error": ["Please make sure your [previous step id] is valid and exist!"]},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            monitor_data['previous_step_obj'] = None

        api_monitor_serializer = APIMonitorSerializer(data=monitor_data)
        monitor_obj = APIMonitor.objects.get(pk=kwargs['pk'])
        if (api_monitor_serializer.is_valid()):
            # Saved
            monitor_obj.name = monitor_data['name']
            monitor_obj.method = monitor_data['method']
            monitor_obj.url = monitor_data['url']
            monitor_obj.schedule = monitor_data['schedule']
            monitor_obj.body_type = monitor_data['body_type']
            monitor_obj.previous_step = monitor_data['previous_step_obj']
            monitor_obj.assertion_type = monitor_data['assertion_type']
            monitor_obj.assertion_value = monitor_data['assertion_value']
            monitor_obj.is_assert_json_schema_only = monitor_data['is_assert_json_schema_only']
            monitor_obj.save()

            # Delete old objects
            APIMonitorQueryParam.objects.filter(monitor=kwargs['pk']).delete()
            APIMonitorHeader.objects.filter(monitor=kwargs['pk']).delete()
            APIMonitorBodyForm.objects.filter(monitor=kwargs['pk']).delete()
            APIMonitorRawBody.objects.filter(monitor=kwargs['pk']).delete()
            AssertionExcludeKey.objects.filter(monitor=kwargs['pk']).delete()

            # Create new query param
            for i in range(len(request.data.get('query_params', []))):
                # Empty key or value will never reach backend, thanks Hugo
                key = request.data.get('query_params')[i]['key']
                value = request.data.get('query_params')[i]['value']
                record = {
                    "monitor": monitor_obj,
                    "key": key,
                    "value": value
                }
                APIMonitorQueryParam.objects.create(**record)

            for i in range(len(request.data.get('headers', []))):
                key = request.data.get('headers')[i]['key']
                value = request.data.get('headers')[i]['value']
                record = {
                    "monitor": monitor_obj,
                    "key": key,
                    "value": value
                }
                APIMonitorHeader.objects.create(**record)

            if (monitor_data['body_type'] == "FORM"):
                for i in range(len(request.data.get('body_form', []))):
                    key = request.data.get('body_form')[i]['key']
                    value = request.data.get('body_form')[i]['value']
                    record = {
                        "monitor": monitor_obj,
                        "key": key,
                        "value": value
                    }
                    APIMonitorBodyForm.objects.create(**record)
            elif (monitor_data['body_type'] == "RAW"):
                record = {
                    'monitor': monitor_obj,
                    'body': request.data['raw_body']
                }
                APIMonitorRawBody.objects.create(**record)

            for i in range(len(request.data.get('exclude_keys', []))):
                key = request.data.get('exclude_keys')[i]['key']
                record = {
                    "monitor": monitor_obj,
                    "exclude_key": key
                }
                AssertionExcludeKey.objects.create(**record)

            serializer = APIMonitorSerializer(monitor_obj)
            return Response(serializer.data)
        else:
            return Response(data={"error": "['Please make sure your [name, method, url, schedule, body_type] is valid']"},status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        monitor_data = self.get_monitor_data_from_request(request)
        api_monitor_serializer = APIMonitorSerializer(data=monitor_data)
        if api_monitor_serializer.is_valid():
            error_log = []
            try:    
                if monitor_data['previous_step_id'] == None or ( try_parse_int(monitor_data['previous_step_id']) and APIMonitor.objects.filter(id=monitor_data['previous_step_id'], user=request.user).exists()):
                    monitor_obj = APIMonitor.objects.create(**monitor_data)
                else:
                    error_log += ["Please make sure your [previous step id] is valid and exist!"]
                    return Response(data={"error": f"{error_log[0]}"}, status=status.HTTP_400_BAD_REQUEST)

                if request.data.get('query_params'):
                    for key_value_pair in request.data.get('query_params'):
                        if 'key' in key_value_pair and 'value' in key_value_pair:
                            key, value = key_value_pair['key'], key_value_pair['value']
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
                        if 'key' in key_value_pair and 'value' in key_value_pair:
                            key, value = key_value_pair['key'], key_value_pair['value']
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
                        if 'key' in key_value_pair and 'value' in key_value_pair:
                            key, value = key_value_pair['key'], key_value_pair['value']
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
                if request.data.get('exclude_keys'):
                    for key_json in request.data.get('exclude_keys'):
                        if 'key' in key_json:
                            key = key_json['key']
                        else:
                            error_log += ["Please make sure you submit correct [exclude key]"]
                            break
                        record = {
                            'monitor': monitor_obj.id,
                            'exclude_key': key,
                        }
                        if AssertionExcludeKeySerializer(data=record).is_valid():
                            record['monitor'] = monitor_obj
                            AssertionExcludeKey.objects.create(**record)
                        else:
                            error_log += ["Please make sure your [exclude key] valid strings!"]
                            break
                assert len(error_log) == 0, error_log
                serialized_obj = APIMonitorSerializer(monitor_obj)
                return Response(data=serialized_obj.data, status=status.HTTP_201_CREATED)
            except AssertionError as e:
                monitor_obj.delete()
                return Response(data={"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"error": "['Please make sure your [name, method, url, schedule, body_type] is valid']"}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve_stats_with_param(self, last_chosen_period_in_hours, increment_in_minutes, monitor):
        last_chosen_period = timezone.now() - timedelta(hours=last_chosen_period_in_hours)
        n_bar = int(last_chosen_period_in_hours * 60 / increment_in_minutes)
        
        success_rate = []
        response_time = []
        for _ in range(n_bar):
            start_time = last_chosen_period
            end_time = last_chosen_period+timedelta(minutes=increment_in_minutes)
            avg_response_time = APIMonitorResult.objects \
                .filter(monitor=monitor, execution_time__gte=start_time, execution_time__lte=end_time) \
                .aggregate(avg=Avg('response_time'))

            avg = 0

            if  avg_response_time["avg"]!=None:
                avg = avg_response_time['avg']

            response_time.append({
                "start_time": start_time,
                "end_time" : end_time,
                "avg": avg
            })

            # Average success rate
            success_count = APIMonitorResult.objects \
                .filter(monitor=monitor, execution_time__gte=start_time, execution_time__lte=end_time) \
                .aggregate(
                    s=Count('success', filter=Q(success=True)), 
                    f=Count('success', filter=Q(success=False)),
                    total=Count('pk'),
                )

            success_rate.append({
                "start_time": start_time,
                "end_time" : end_time,
                "success": success_count['s'],
                "failed" : success_count['f']
            })
            last_chosen_period = last_chosen_period+timedelta(minutes=increment_in_minutes)
        
        return success_rate, response_time

    def retrieve(self, request, pk=None):          
        queryset = self.filter_queryset(self.get_queryset())
        monitor = get_object_or_404(queryset,pk=pk)
        stats_range = self.request.query_params.get("range")
        
        response_time = []
        success_rate = []
        
        cache_key = CACHE_KEY_API_MONITOR_DETAIL_STATS.format(monitor.id, stats_range)
        cache_stats = get_cache_value(cache_key)
        if cache_stats:
            cache_stats = json.loads(cache_stats)
            success_rate = cache_stats['success_rate']
            response_time = cache_stats['response_time']
        else:
            if(stats_range=="30MIN"):
                success_rate, response_time = self.retrieve_stats_with_param(0.5, 1, monitor)
            elif(stats_range=="60MIN"):
                success_rate, response_time = self.retrieve_stats_with_param(1, 2, monitor)
            elif(stats_range=="180MIN"):
                success_rate, response_time = self.retrieve_stats_with_param(3, 5, monitor)
            elif(stats_range=="360MIN"):
                success_rate, response_time = self.retrieve_stats_with_param(6, 10, monitor)
            elif(stats_range=="720MIN"):
                success_rate, response_time = self.retrieve_stats_with_param(12, 20, monitor)
            elif(stats_range=="1440MIN"):
                success_rate, response_time = self.retrieve_stats_with_param(24, 30, monitor)
                
            set_cache_value(cache_key, json.dumps({
                'success_rate': APIMonitorDetailSuccessRateSerializer(success_rate, many=True).data,
                'response_time': APIMonitorDetailResponseTimeSerializer(response_time, many=True).data,
            }), timeout=60)

        monitor.success_rate = success_rate
        monitor.response_time = response_time

        serializer = APIMonitorRetrieveSerializer(monitor)
        return Response(serializer.data)
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        last_24_hour = timezone.now() - timedelta(days=1)
        
        # Append summary to each monitor
        for monitor in queryset:
            cache_key = CACHE_KEY_API_MONITOR_LIST.format(monitor.id)
            
            cache_monitor = get_cache_value(cache_key)
            if cache_monitor:
                cache_monitor = json.loads(cache_monitor)
                
                monitor.avg_response_time = cache_monitor['avg_response_time']
                monitor.success_rate = cache_monitor['success_rate']
                monitor.success_rate_history = cache_monitor['success_rate_history']
                monitor.last_result = cache_monitor['last_result']
                continue
                
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
            success_rate_history = []
            last_24_hour_per_monitor = last_24_hour
            for _ in range(24):
                start_time = last_24_hour_per_monitor
                end_time = last_24_hour_per_monitor + timedelta(hours=1)
                
                success_count = APIMonitorResult.objects \
                    .filter(monitor=monitor, execution_time__gte=start_time, execution_time__lte=end_time) \
                    .aggregate(
                        s=Count('success', filter=Q(success=True)), 
                        f=Count('success', filter=Q(success=False)),
                        total=Count('pk'),
                    )
            
                success_rate_history.append({
                    'start_time': start_time,
                    'end_time': end_time,
                    'success': success_count['s'],
                    'failed': success_count['f'],
                })
                last_24_hour_per_monitor += timedelta(hours=1)
           
            monitor.success_rate_history = success_rate_history
            
            # Last result 
            last_result = APIMonitorResult.objects.filter(monitor=monitor).last()
            monitor.last_result = last_result
            
            serializer_obj = APIMonitorListSerializer(monitor)
            set_cache_value(cache_key, json.dumps(serializer_obj.data), timeout=60)
       
        serializer = APIMonitorListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False,methods=["GET"])
    def stats(self, request):
        queryset = self.filter_queryset(self.get_queryset())
    
        response_time= []
        success_rate = []
        
        cache_key = CACHE_KEY_API_MONITOR_STATS.format(request.user.id)
        cache_stats = get_cache_value(cache_key)
        if cache_stats:
            cache_stats = json.loads(cache_stats)
            success_rate = cache_stats['success_rate']
            response_time = cache_stats['response_time']
        else:
            last_chosen_period = timezone.now() - timedelta(hours=24)
            for _ in range(24):
                start_time = last_chosen_period
                end_time = last_chosen_period+timedelta(hours=1)
                avg_response_time = APIMonitorResult.objects \
                    .filter(monitor__user=request.user, execution_time__gte=start_time, execution_time__lte=end_time) \
                    .aggregate(avg=Avg('response_time'))

                avg = 0

                if  avg_response_time["avg"]!=None:
                    avg = avg_response_time['avg']

                response_time.append({
                    "start_time": start_time,
                    "end_time" : end_time,
                    "avg": avg
                })

                # Average success rate
                success_count = APIMonitorResult.objects \
                    .filter(monitor__user=request.user, execution_time__gte=start_time, execution_time__lte=end_time) \
                    .aggregate(
                        s=Count('success', filter=Q(success=True)), 
                        f=Count('success', filter=Q(success=False)),
                        total=Count('pk'),
                    )

                success_rate.append({
                    "start_time": start_time,
                    "end_time" : end_time,
                    "success": success_count['s'],
                    "failed" : success_count['f']
                })
                last_chosen_period = last_chosen_period+timedelta(hours=1)
            
            set_cache_value(cache_key, json.dumps({
                'success_rate': APIMonitorDetailSuccessRateSerializer(success_rate, many=True).data,
                'response_time': APIMonitorDetailResponseTimeSerializer(response_time, many=True).data,
            }), timeout=60)

        queryset.success_rate = success_rate
        queryset.response_time = response_time
        serializer = APIMonitorDashboardSerializer(queryset)
        return Response(serializer.data)
