import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import requests
import time

from apimonitor.models import APIMonitor, APIMonitorBodyForm, APIMonitorHeader, APIMonitorQueryParam, APIMonitorRawBody, APIMonitorResult


class Command(BaseCommand):
    help = 'Run API Monitor Cron'

    def handle(self, *args, **kwargs):
        schedule_in_seconds = {
            '1MIN': 60,
            '2MIN': 120,
            '3MIN': 180,
            '5MIN': 300,
            '10MIN': 600,
            '15MIN': 900,
            '30MIN': 1800,
            '60MIN': 3600,
        }
        
        while True:
            api_monitors = APIMonitor.objects.all()
            for monitor in api_monitors:
                result_filter_time = timezone.now() - timedelta(seconds=schedule_in_seconds[monitor.schedule])
                
                last_result = APIMonitorResult.objects.filter(
                    monitor=monitor, 
                    execution_time__gte=result_filter_time
                ).exists()
                
                if last_result:
                    continue
                
                # Prepare headers
                request_headers = {}
                headers = APIMonitorHeader.objects.filter(monitor=monitor)
                for header in headers:
                    request_headers[header.key] = header.value
                    
                # Prepare request body
                request_body = {}
                if monitor.body_type == 'FORM':
                    forms = APIMonitorBodyForm.objects.filter(monitor=monitor)
                    for form in forms:
                        request_body[form.key] = form.value
                elif monitor.body_type == 'RAW':
                    try:
                        raw_body = APIMonitorRawBody.objects.get(monitor=monitor)
                        request_body = raw_body.body
                    except APIMonitorRawBody.DoesNotExist:
                        pass
                elif monitor.body_type == 'EMPTY':
                    request_body = None
                    
                # Prepare query params
                request_params = {}
                query_params = APIMonitorQueryParam.objects.filter(monitor=monitor)
                for param in query_params:
                    request_params[param.key] = param.value
                        
                resp = None
                exception = ''
                
                start = time.perf_counter()
                try:
                    if monitor.method == 'GET':
                        resp = requests.get(monitor.url, params=request_params, headers=request_headers)
                    elif monitor.method == 'POST':
                        resp = requests.post(monitor.url, params=request_params, data=request_body, headers=request_headers)
                    elif monitor.method == 'PATCH':
                        resp = requests.patch(monitor.url, params=request_params, data=request_body, headers=request_headers)
                    elif monitor.method == 'PUT':
                        resp = requests.put(monitor.url, params=request_params, data=request_body, headers=request_params)
                    elif monitor.method == 'DELETE':
                        resp = requests.delete(monitor.url, params=request_params, data=request_body, headers=request_headers)
                except Exception as e:
                    exception = str(e)
                request_time = (time.perf_counter() - start) * 1000 # Convert from s to ms
                
                success = False
                resp_content = ''
                if resp is not None:
                    if resp.status_code >= 200 and resp.status_code <= 299:
                        success = True
                    resp_content = resp.content.decode('utf-8')
                    
                execution_time = timezone.localtime()
                APIMonitorResult.objects.create(
                    monitor=monitor,
                    execution_time=execution_time,
                    date=execution_time.date(),
                    hour=execution_time.hour,
                    minute=execution_time.minute,
                    response_time=request_time,
                    success=success,
                    log_response=resp_content,
                    log_error=exception,
                )

            # Add deloy before next check
            time.sleep(60)
