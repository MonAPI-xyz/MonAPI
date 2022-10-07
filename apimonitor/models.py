from django.db import models
from django.contrib.auth.models import User


class APIMonitor(models.Model):
    method_choices = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PATCH', 'PATCH'),
        ('PUT', 'PUST'),
        ('DELETE', 'DELETE'),
    ]
    
    body_type_choices = [
        ('EMPTY', 'EMPTY'),
        ('FORM', 'FORM'),
        ('RAW', 'RAW')
    ]
    
    schedule_choices = [
        ('1MIN', '1 Minute'),
        ('2MIN', '2 Minute'),
        ('3MIN', '3 Minute'),
        ('5MIN', '5 Minute'),
        ('10MIN', '10 Minute'),
        ('15MIN', '15 Minute'),
        ('30MIN', '30 Minute'),
        ('60MIN', '60 Minute'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    method = models.CharField(max_length=16, choices=method_choices)
    url = models.CharField(max_length=512)
    schedule = models.CharField(max_length=64, choices=schedule_choices)
    body_type = models.CharField(max_length=16, choices=body_type_choices)
    
    
class APIMonitorQueryParam(models.Model):
    monitor = models.ForeignKey(APIMonitor, on_delete=models.CASCADE, related_name='query_params')
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=1024)
    
    
class APIMonitorHeader(models.Model):
    monitor = models.ForeignKey(APIMonitor, on_delete=models.CASCADE, related_name='headers')
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=1024)
    
    
class APIMonitorBodyForm(models.Model):
    monitor = models.ForeignKey(APIMonitor, on_delete=models.CASCADE, related_name='body_form')
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=1024)


class APIMonitorRawBody(models.Model):
    monitor = models.OneToOneField(APIMonitor, on_delete=models.CASCADE, related_name='raw_body')
    body = models.TextField()


class APIMonitorResult(models.Model):
    monitor = models.ForeignKey(APIMonitor, on_delete=models.CASCADE, related_name='results')
    execution_time = models.DateTimeField()
    date = models.DateField()
    hour = models.IntegerField()
    minute = models.IntegerField()
    response_time = models.IntegerField() # in miliseconds
    success = models.BooleanField()
    log_response = models.TextField()
    log_error = models.TextField()
