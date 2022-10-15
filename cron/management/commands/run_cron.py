import os
import requests
import time
import threading
import queue
from datetime import timedelta

from django.utils import timezone
from django.core.management.base import BaseCommand

from apimonitor.models import APIMonitor, APIMonitorBodyForm, APIMonitorHeader, APIMonitorQueryParam, APIMonitorRawBody, APIMonitorResult

# Mock this function to interrupt the cron function
def mock_cron_interrupt():
    pass

class Command(BaseCommand):
    help = 'Run API Monitor Cron'
    
    q = queue.Queue()
    stop_signal = threading.Event()
    
    def get_monitor_id_from_queue(self):
        while True:
            try:
                monitor_id = self.q.get(block=False)
                return monitor_id
            except queue.Empty:
                if self.stop_signal.is_set():
                    return None
            time.sleep(0.2)
    
    def worker(self):
        while True:
            # Prevent halt worker
            try:
                monitor_id = self.get_monitor_id_from_queue()
                if monitor_id == None:
                    return
                
                execution_time = timezone.localtime()
                print(f"[{timezone.now()}] Running cron for monitor id:{monitor_id}")
                monitor = APIMonitor.objects.get(id=monitor_id)
                
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
                        resp = requests.get(monitor.url, params=request_params, headers=request_headers, timeout=30)
                    elif monitor.method == 'POST':
                        resp = requests.post(monitor.url, params=request_params, data=request_body, headers=request_headers, timeout=30)
                    elif monitor.method == 'PATCH':
                        resp = requests.patch(monitor.url, params=request_params, data=request_body, headers=request_headers, timeout=30)
                    elif monitor.method == 'PUT':
                        resp = requests.put(monitor.url, params=request_params, data=request_body, headers=request_params, timeout=30)
                    elif monitor.method == 'DELETE':
                        resp = requests.delete(monitor.url, params=request_params, data=request_body, headers=request_headers, timeout=30)
                except Exception as e:
                    exception = str(e)
                request_time = (time.perf_counter() - start) * 1000 # Convert from s to ms
                
                success = False
                status_code = -1
                resp_content = ''
                if resp is not None:
                    if resp.status_code >= 200 and resp.status_code <= 299:
                        success = True
                    resp_content = resp.content.decode('utf-8', errors='ignore')
                    status_code = resp.status_code
                    
                APIMonitorResult.objects.create(
                    monitor=monitor,
                    execution_time=execution_time,
                    response_time=request_time,
                    success=success,
                    status_code=status_code,
                    log_response=resp_content,
                    log_error=exception,
                )
                print(f"[{timezone.now()}] Done run cron for monitor id:{monitor_id}")
                self.q.task_done()
            except:
                pass

    def handle(self, *args, **kwargs):
        # Run consumer worker
        self.stop_signal.clear()
        thread_pool = []
        last_triggered = {}
        
        consumer_count = 3
        try:
            consumer_count = int(os.getenv('CRON_THREAD_COUNT', 3))
        except ValueError:
            pass
        
        for _ in range(consumer_count):
            consumer = threading.Thread(target=self.worker)
            consumer.start()
            thread_pool.append(consumer)

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
        
        try:
            # Fill last_triggered
            api_monitors = APIMonitor.objects.all()
            for monitor in api_monitors:
                exists = APIMonitorResult.objects.filter(monitor=monitor).exists()
                if exists:
                    last_result = APIMonitorResult.objects.filter(monitor=monitor).last()
                    last_triggered[monitor.id] = last_result.execution_time
                
            # Cron loop function
            while True:
                last_run = timezone.now()
                api_monitors = APIMonitor.objects.all()
                for monitor in api_monitors:
                    result_filter_time = last_run - timedelta(seconds=schedule_in_seconds[monitor.schedule])
                    if monitor.id in last_triggered and result_filter_time < last_triggered[monitor.id]:
                        continue
                    
                    last_triggered[monitor.id] = last_run
                    self.q.put(monitor.id)
                    
                # Add delay before next check
                mock_cron_interrupt()
                next_run = last_run + timedelta(seconds=60) 
                sleep_duration = (next_run - timezone.now()).total_seconds()
                time.sleep(max(sleep_duration, 0))  
        except BaseException as e:
            # Gracefully shutdown thread worker
            self.q.join()
            self.stop_signal.set()
            for thread in thread_pool:
                thread.join()            
            raise e
