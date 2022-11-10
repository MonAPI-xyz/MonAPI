import requests
from rest_framework import status, views
from rest_framework.response import Response

from apitest.serializers import (APITestQueryParamSerializer, APITestHeaderSerializer, APITestBodyFormSerializer)

class APITestView(views.APIView):
    def post(self, request, format=None):
        monitor_data = {
            'method': request.data.get('method'),
            'url': request.data.get('url'),
            'body_type': request.data.get('body_type'),
            'query_params': {},
            'headers' : {},
            'body' : {},            
        }
        error_log = []
        try:
            if request.data.get('query_params'):
                for key_value_pair in request.data.get('query_params'):
                    if 'key' in key_value_pair and 'value' in key_value_pair:
                        key, value = key_value_pair['key'], key_value_pair['value']
                    else:
                        error_log += ["Please make sure you submit correct [query params]"]
                        break
                    record = {
                        'key': key,
                        'value': value
                    }
                    if APITestQueryParamSerializer(data=record).is_valid():
                        monitor_data['query_params'][key] = value
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
                        'key': key,
                        'value': value
                    }
                    if APITestHeaderSerializer(data=record).is_valid():
                        monitor_data['headers'][key] = value
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
                        'key': key,
                        'value': value
                    }
                    if APITestBodyFormSerializer(data=record).is_valid():
                        monitor_data['body'][key] = value
                    else:
                        error_log += ["Please make sure your [body form] key and value are valid strings!"]
                        break
            elif request.data.get('body_type') == 'RAW':
                monitor_data['body']=request.data["raw_body"]

            assert len(error_log) == 0, error_log

            resp = None
        
            try:
                print(f"""
                    url = {monitor_data['url']}
                    params = {monitor_data['query_params']}
                    headers = {monitor_data['headers']}
                    data = {monitor_data['body']}
                """)
                if monitor_data['method'] == 'GET':
                    resp = requests.get(monitor_data['url'], params=monitor_data['query_params'], headers=monitor_data['headers'], timeout=30)
                elif monitor_data['method'] == 'POST':
                    resp = requests.post(monitor_data['url'], params=monitor_data['query_params'], data=monitor_data['body'], headers=monitor_data['headers'], timeout=30)
                elif monitor_data['method'] == 'PATCH':
                    resp = requests.patch(monitor_data['url'], params=monitor_data['query_params'], data=monitor_data['body'], headers=monitor_data['headers'], timeout=30)
                elif monitor_data['method'] == 'PUT':
                    resp = requests.put(monitor_data['url'], params=monitor_data['query_params'], data=monitor_data['body'], headers=monitor_data['headers'], timeout=30)
                elif monitor_data['method'] == 'DELETE':
                    resp = requests.delete(monitor_data['url'], params=monitor_data['query_params'], data=monitor_data['body'], headers=monitor_data['headers'], timeout=30)
            except Exception as e:
                error_log += [str(e)]

            assert len(error_log) == 0, error_log

            return Response({
                'response': resp.content.decode('utf-8', errors='ignore')
            })

        except AssertionError as e:
            return Response(data={"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
    