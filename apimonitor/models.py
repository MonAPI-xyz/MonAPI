from io import open_code
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

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
    
    assertion_type_choices = [
        ('DISABLED', 'Disabled'),
        ('TEXT', 'Text'),
        ('JSON', 'JSON'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    method = models.CharField(max_length=16, choices=method_choices)
    url = models.CharField(max_length=512)
    schedule = models.CharField(max_length=64, choices=schedule_choices)
    body_type = models.CharField(max_length=16, choices=body_type_choices)
    previous_step = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    assertion_type = models.CharField(max_length=16, choices=assertion_type_choices, default='DISABLED')
    assertion_value = models.TextField(blank=True)
    is_assert_json_schema_only = models.BooleanField(default=False)
    
    
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
    response_time = models.IntegerField() # in miliseconds
    success = models.BooleanField()
    status_code = models.IntegerField()
    log_response = models.TextField()
    log_error = models.TextField()
    
    class Meta:
        indexes = [
            models.Index(fields=['monitor', 'execution_time'], name='result_time_index'),
            models.Index(fields=['monitor', 'success'], name='result_success_index'),
        ]
        
        
class AssertionExcludeKey(models.Model):
    monitor = models.ForeignKey(APIMonitor, on_delete=models.CASCADE, related_name='exclude_keys')
    exclude_key = models.CharField(max_length=1024)
    

class AlertsConfiguration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Slack config
    is_slack_active = models.BooleanField(default=False)
    slack_token = models.CharField(max_length=256, blank=True, default="")
    slack_channel_id = models.CharField(max_length=256, blank=True, default="")
    
    # Discord config
    is_discord_active = models.BooleanField(default=False)
    discord_bot_token = models.CharField(max_length=256, blank=True, default="")
    discord_guild_id = models.CharField(max_length=256, blank=True, default="")
    discord_channel_id = models.CharField(max_length=256, blank=True, default="")
    
    # Pagerduty config
    is_pagerduty_active = models.BooleanField(default=False)
    pagerduty_api_key = models.CharField(max_length=256, blank=True, default="")
    pagerduty_default_from_email = models.CharField(max_length=256, blank=True, default="")
    
    # Email config
    is_email_active = models.BooleanField(default=False)
    email_host = models.CharField(max_length=1024, blank=True, default="")
    email_port = models.IntegerField(null=True, blank=True)
    email_username = models.CharField(max_length=1024, blank=True, default="")
    email_password = models.CharField(max_length=1024, blank=True, default="")
    email_use_tls = models.BooleanField(default=False)
    email_use_ssl = models.BooleanField(default=False)

    # Threshold config
    time_window_choices = [
        ('1H', '1 Hour'),
        ('2H', '2 Hour'),
        ('3H', '3 Hour'),
        ('6H', '6 Hour'),
        ('12H', '12 Hour'),
        ('24H', '24 Hour')
    ]
    threshold_pct = models.IntegerField(default=100, validators=[
        MinValueValidator(1),
        MaxValueValidator(100)
    ])
    time_window = models.CharField(max_length=16, choices=time_window_choices, default='1H')
