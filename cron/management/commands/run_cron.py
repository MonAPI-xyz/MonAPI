import os
import requests
import time
import threading
import queue
import re
import json
from datetime import timedelta

from django.utils import timezone
from django.core.management.base import BaseCommand
from deepdiff import DeepDiff

from apimonitor.models import APIMonitor, APIMonitorBodyForm, APIMonitorHeader, APIMonitorQueryParam, APIMonitorRawBody, APIMonitorResult, AssertionExcludeKey

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
    
    # Access dictionary with key a.b.c or a.b.c[0] or a.b[0].c
    def access_dict_with_key(self, key, source):
        key_part = key.split('.', 1)
        current_key = key_part[0]
        res = None
        
        if not isinstance(source, dict):
            return False
        
        array_idx = re.findall("\[\d\]$", current_key)
        if len(array_idx) == 1:
            current_key = current_key.replace(array_idx[0], '')
            if current_key not in source:
                return False
            
            if not isinstance(source[current_key], list):
                return False
            
            array_idx_num = int(array_idx[0].strip('[]'))
            if len(source[current_key]) < array_idx_num + 1:
                return False
            
            res = source[current_key][array_idx_num]
        else:
            if current_key not in source:
                return False
            
            res = source[current_key]
            
        if len(key_part) > 1:
            return self.access_dict_with_key(key_part[1], res)
        return str(res)

    def replace_string_with_json_result(self, text, dict):
        if dict is None:
            return text

        result = re.findall("{{.+?}}", text)
        for match in result:
            key = match.strip("{}")
            value = self.access_dict_with_key(key, dict)
            if value == False:
                raise KeyError(f"Value not found while accessing with key \"{key}\"")
            text = text.replace(match, value)
        return text

    def run_api_monitor_assertions(self, monitor_id, response):
        monitor = APIMonitor.objects.get(id=monitor_id)
        if monitor.assertion_type == 'TEXT' and response != monitor.assertion_value:
            raise AssertionError('Assertion text failed')
        elif monitor.assertion_type == 'JSON':
            try:
                api_response = json.loads(response) 
            except json.decoder.JSONDecodeError:
                raise AssertionError('Failed to decode JSON api response')
            
            try:
                assertion_value = json.loads(monitor.assertion_value)
            except json.decoder.JSONDecodeError:
                raise AssertionError('Failed to decode JSON monitor assertions value')
            
            # Assertion exclude keys
            ddiff_exclude_path = []
            exclude_keys = AssertionExcludeKey.objects.filter(monitor=monitor)
            for key in exclude_keys:
                key = key.exclude_key.split('.')
                res_key = 'root'
                for key_part in key:
                    array_idx = re.findall("\[[\d]\]$", key_part)
                    if len(array_idx) == 1:
                        key_part = key_part.replace(array_idx[0], '')
                        res_key += f"['{key_part}']{array_idx[0]}"
                    else:
                        res_key += f"['{key_part}']"
                ddiff_exclude_path.append(res_key)
            
            ddiff = DeepDiff(assertion_value, api_response, exclude_paths=ddiff_exclude_path)
            
            diff_result = ""
            if not monitor.is_assert_json_schema_only:
                if 'type_changes' in ddiff:
                    for k,v in ddiff['type_changes'].items():
                        diff_result += f"Different type detected on {k}, expected \"{v['old_value']}\" ({v['old_type']}) but found \"{v['new_value']}\" ({v['new_type']})\n"
                if 'values_changed' in ddiff:
                    for k,v in ddiff['values_changed'].items():
                        diff_result += f"Different value detected on {k}, expected \"{v['old_value']}\" but found \"{v['new_value']}\"\n"
            if 'dictionary_item_added' in ddiff:
                diff_result += f"New key detected with keys {ddiff['dictionary_item_added']}\n"
            if 'dictionary_item_removed' in ddiff:
                diff_result += f"Missing key detected with keys {ddiff['dictionary_item_removed']}\n"
            if 'iterable_item_added' in ddiff:
                diff_result += f"Found iterable item added with keys {ddiff['iterable_item_added'].keys()}\n"
            if 'iterable_item_removed' in ddiff:
                diff_result += f"Found iterable item removed with keys {ddiff['iterable_item_removed'].keys()}\n"

            if diff_result != "":
                raise AssertionError(diff_result.strip('\n'))
            
    def run_api_monitor_request(self, monitor_id, monitor_history):
        monitor_history.append(monitor_id)
        
        monitor = APIMonitor.objects.get(id=monitor_id)
        previous_json = None
        result = APIMonitorResult(
            monitor=monitor,
            success=False,
            status_code=-1,
            log_response="",
            log_error="",
        )
        
        # Run previous step of api monitor
        if monitor.previous_step != None:
            # Limit 10 monitor
            if len(monitor_history) >= 10:
                return APIMonitorResult(
                    monitor=monitor,
                    success=False,
                    status_code=-1,
                    log_response="",
                    log_error=f"Depth limit of previous step API monitor reached (maximum: 10)"
                )
                
            # Check if infinite recursion on api monitor detected
            if monitor.previous_step.id in monitor_history:
                return APIMonitorResult(
                    monitor=monitor,
                    success=False,
                    status_code=-1,
                    log_response="",
                    log_error=f"Request aborted due to recursion of API monitor steps"
                )
                
            result = self.run_api_monitor_request(monitor.previous_step.id, monitor_history)
            if not result.success:
                return APIMonitorResult(
                    monitor=monitor,
                    success=False,
                    status_code=result.status_code,
                    log_response=result.log_response,
                    log_error=f"Error on previous step: {result.monitor.name}\n" + result.log_error,
                )
                
            # Extract json from log response if possible
            try:
                previous_json = json.loads(result.log_response)
            except json.decoder.JSONDecodeError:
                pass
        
        try:
            # Prepare headers
            request_headers = {}
            headers = APIMonitorHeader.objects.filter(monitor=monitor)
            for header in headers:
                header_key = self.replace_string_with_json_result(header.key, previous_json)
                header_value = self.replace_string_with_json_result(header.value, previous_json)
                request_headers[header_key] = header_value
                
            # Prepare request body
            request_body = {}
            if monitor.body_type == 'FORM':
                forms = APIMonitorBodyForm.objects.filter(monitor=monitor)
                for form in forms:
                    form_key = self.replace_string_with_json_result(form.key, previous_json)
                    form_value = self.replace_string_with_json_result(form.value, previous_json)
                    request_body[form_key] = form_value
            elif monitor.body_type == 'RAW':
                try:
                    raw_body = APIMonitorRawBody.objects.get(monitor=monitor)
                    request_body = self.replace_string_with_json_result(raw_body.body, previous_json)
                except APIMonitorRawBody.DoesNotExist:
                    pass
            elif monitor.body_type == 'EMPTY':
                request_body = None
                
            # Prepare query params
            request_params = {}
            query_params = APIMonitorQueryParam.objects.filter(monitor=monitor)
            for param in query_params:
                params_key = self.replace_string_with_json_result(param.key, previous_json)
                params_value =  self.replace_string_with_json_result(param.value, previous_json)
                request_params[params_key] = params_value
        except KeyError as e:
            return APIMonitorResult(
                monitor=monitor,
                success=False,
                status_code=result.status_code,
                log_response=result.log_response,
                log_error=f"Error while preparing API monitor params: {str(e)}\n" + result.log_error,
            )
                
        resp = None
        
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
            result.log_error = str(e)
        
        if resp is not None:
            if resp.status_code >= 200 and resp.status_code <= 299:
                result.success = True
            result.log_response = resp.content.decode('utf-8', errors='ignore')
            result.status_code = resp.status_code
            
        # Run assertions only on root monitor
        if len(monitor_history) == 1:
            try:
                self.run_api_monitor_assertions(monitor.id, result.log_response)
            except AssertionError as e:
                result.success = False
                result.log_error = str(e)
                
        return result
    
    
    def worker(self):
        while True:
            # Prevent halt worker
            try:
                monitor_id = self.get_monitor_id_from_queue()
                if monitor_id == None:
                    return
                
                print(f"[{timezone.now()}] Running cron for monitor id:{monitor_id}")
                
                execution_time = timezone.localtime()
                start = time.perf_counter()
                
                api_monitor_result = self.run_api_monitor_request(monitor_id, [])
                
                process_time = (time.perf_counter() - start) * 1000 # Convert from s to ms
                api_monitor_result.execution_time = execution_time
                api_monitor_result.response_time = process_time
                api_monitor_result.save()
                
                print(f"[{timezone.now()}] Done run cron for monitor id:{monitor_id}")
                self.q.task_done()
            except Exception as e:
                print(e)

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
