import os
import requests
import time
import threading
import queue
from datetime import timedelta, timezone as tzdt

from django.core.mail import get_connection
from django.template.loader import render_to_string
from django.utils import timezone
from django.db.models import Count, Q
from django.core.management.base import BaseCommand

from apimonitor.models import APIMonitor, APIMonitorResult, AlertsConfiguration
from login.models import TeamMember

from discord_webhook import DiscordWebhook, DiscordEmbed
# Mock this function to interrupt the cron function
def mock_cron_interrupt():
    pass


class Command(BaseCommand):
    help = 'Run Cron Alerts'
    
    queue = {}
    channels = ['slack', 'discord', 'pagerduty', 'email']
    
    stop_signal = threading.Event()

    def get_success_rate(self, monitor):
        time_window_in_seconds = {
            '1H': 3600,
            '2H': 7200,
            '3H': 10800,
            '6H': 21600,
            '12H': 43200,
            '24H': 86400,
        }
        
        alerts_config, _ = AlertsConfiguration.objects.get_or_create(team=monitor.team)
        end_time = timezone.now()
        start_time = end_time - timedelta(seconds=time_window_in_seconds[alerts_config.time_window])

        # Average success rate
        success_count = APIMonitorResult.objects \
            .filter(monitor=monitor, execution_time__gte=start_time) \
            .aggregate(
            s=Count('success', filter=Q(success=True)),
            f=Count('success', filter=Q(success=False)),
            total=Count('pk'),
        )

        success_rate = 100
        if success_count['total'] != 0:
            success_rate = success_count['s'] / (success_count['total']) * 100

        formatted_success_rate = round(float(success_rate), 2)
        formatted_start_time = start_time.astimezone(tzdt(timedelta(hours=+alerts_config.utc))).strftime("%d %b %Y, %H:%M:%S %Z")
        formatted_end_time = end_time.astimezone(tzdt(timedelta(hours=+alerts_config.utc))).strftime("%d %b %Y, %H:%M:%S %Z")

        return formatted_success_rate , formatted_start_time, formatted_end_time
    
    def get_monitor_id_from_queue(self, type):
        while True:
            try:
                q = self.queue[type]
                monitor_id = q.get(block=False)
                return monitor_id
            except queue.Empty:
                if self.stop_signal.is_set():
                    return None
            time.sleep(0.2)
            
    def put_monitor_id_into_queue(self, monitor_id):
        for channel in self.channels:
            q = self.queue[channel]
            q.put(monitor_id)
            
    def send_alert_slack(self, monitor_id, success_rate, start_time, end_time):
        monitor = APIMonitor.objects.get(id=monitor_id)
        monitor_link = os.getenv('FRONTEND_URL') + f"/{monitor_id}/detail/"
        alerts_config, _ = AlertsConfiguration.objects.get_or_create(team=monitor.team)
        requests.post('https://slack.com/api/chat.postMessage', json=
        {
            "channel": alerts_config.slack_channel_id,
            "text": f"Success rate monitor <{monitor_link}|{monitor.name}> is dropping below {alerts_config.threshold_pct}%\nCurrent success rate from {start_time} - {end_time}: {success_rate}%\nYour monitor URL: {monitor.url}\nMethod: {monitor.method}"
        }, headers={
            "Authorization": f"Bearer {alerts_config.slack_token}",
            "Content-Type": "application/json",
        })
    
    def send_alert_discord(self, monitor_id, success_rate, start_time, end_time):
        monitor = APIMonitor.objects.get(id=monitor_id)
        alerts_config, _ = AlertsConfiguration.objects.get_or_create(team=monitor.team)
        discord_webhook_url = alerts_config.discord_webhook_url
        webhook = DiscordWebhook(url=discord_webhook_url, rate_limit_retry=True)
        embed = DiscordEmbed(title=f"Your API Monitor ({monitor.name}) Recently failed!",
                             description=f"Your API Monitor failed to reach {alerts_config.threshold_pct}% success rate",
                             url=os.getenv('FRONTEND_URL') + f"/{monitor_id}/detail/"
                             )

        embed.add_embed_field(name='Threshold', value=f"{alerts_config.threshold_pct}%")
        embed.add_embed_field(name=f'Current Success rate', value=f"{success_rate}%")
        embed.add_embed_field(name='Success rate range', value=f"{start_time} - {end_time}")
        embed.add_embed_field(name='Method', value=f"{monitor.method}")
        embed.add_embed_field(name="Url", value=f"{monitor.url}")
        embed.set_timestamp()

        webhook.add_embed(embed)
        webhook.execute()
    
    def send_alert_pagerduty(self, monitor_id, success_rate, start_time, end_time):
        monitor = APIMonitor.objects.get(id=monitor_id)
        alerts_config, _ = AlertsConfiguration.objects.get_or_create(team=monitor.team)
        
        requests.post('https://api.pagerduty.com/incidents', json={
            "incident": {
                "type": "incident",
                "title": f"Success rate monitor {monitor.name} is dropping below {alerts_config.threshold_pct}%",
                "service": {
                    "id": alerts_config.pagerduty_service_id,
                    "type": "service_reference"
                },
                "body": {
                    "type": "incident_body",
                    "details": f"Success rate is dropping below {alerts_config.threshold_pct}%\nCurrent success rate from {start_time} - {end_time}: {success_rate}"
                }
            }
        }, headers={
            "Authorization": f"Token token={alerts_config.pagerduty_api_key}",
            "From": alerts_config.pagerduty_default_from_email,
            "Content-Type": "application/json",
            "Accept": "application/vnd.pagerduty+json;version=2",
        })
    
    def send_alert_email(self, monitor_id, success_rate, start_time, end_time):
        monitor = APIMonitor.objects.get(id=monitor_id)
        alerts_config, _ = AlertsConfiguration.objects.get_or_create(team=monitor.team)
        error_logs_link = f"{os.environ.get('FRONTEND_URL', '')}/error-logs/"

        email_subject = f"Alerts on monitor {monitor.name}! - MonAPI"
        email_content = f'''
            Success rate monitor {monitor.name} is dropping below {alerts_config.threshold_pct}%\n
            Current success rate from {start_time} - {end_time} is {success_rate}%
            You can check the error logs in\n
            {error_logs_link}
            '''
        from_email = f"{alerts_config.email_name} <{alerts_config.email_address}>"
        email_content_html = render_to_string('email/alerts.html', {
                'api_monitor_name': monitor.name,
                'threshold_pct': alerts_config.threshold_pct,
                'error_logs_link': error_logs_link,
                'success_rate': success_rate,
                'start_time': start_time,
                'end_time': end_time,
            })

        with get_connection(
            host = alerts_config.email_host, 
            port = alerts_config.email_port, 
            username = alerts_config.email_username, 
            password = alerts_config.email_password, 
            use_tls = alerts_config.email_use_tls,
            use_ssl = alerts_config.email_use_ssl
        ) as connection:
            team_members = TeamMember.objects.filter(team=monitor.team)
            for member in team_members:
                member.user.email_user(
                    email_subject,
                    email_content,
                    from_email,
                    fail_silently=False,
                    connection=connection,
                    html_message=email_content_html,
                )
    
    def worker(self, type):
        monitor_id = None
        
        while True:
            try:
                monitor_id = self.get_monitor_id_from_queue(type)
                if monitor_id == None:
                    return
                
                print(f"[{timezone.now()}] Send {type} alert for monitor id:{monitor_id}")
                
                monitor = APIMonitor.objects.get(id=monitor_id)
                success_rate, start_time, end_time = self.get_success_rate(monitor)
                alerts_config, _ = AlertsConfiguration.objects.get_or_create(team=monitor.team)
                
                if type == 'slack' and alerts_config.is_slack_active:
                    self.send_alert_slack(monitor_id, success_rate, start_time, end_time)
                elif type == 'discord' and alerts_config.is_discord_active:
                    self.send_alert_discord(monitor_id, success_rate,start_time, end_time)
                elif type == 'pagerduty' and alerts_config.is_pagerduty_active:
                    self.send_alert_pagerduty(monitor_id, success_rate,start_time, end_time)
                elif type == 'email' and alerts_config.is_email_active:
                    self.send_alert_email(monitor_id, success_rate,start_time, end_time)    
                
                print(f"[{timezone.now()}] Done send {type} alert for monitor id:{monitor_id}")
                   
            except Exception as e:
                print(e)
            
            if monitor_id != None:
                self.queue[type].task_done()  
            
    def handle(self, *args, **kwargs):
        self.stop_signal.clear()
        thread_pool = []
        
        consumer_count = 1
        try:
            consumer_count = int(os.getenv('CRON_ALERTS_THREAD_COUNT', 1))
        except ValueError:
            pass
        
        cron_interval = int(os.environ.get('CRON_INTERVAL_IN_SECONDS', 60))
        
        for channel in self.channels:
            self.queue[channel] = queue.Queue()
            for _ in range(consumer_count):
                consumer = threading.Thread(target=self.worker, args=[channel])
                consumer.start()
                thread_pool.append(consumer)
        
        try:
            # Cron loop function
            while True:
                last_run = timezone.now()
                api_monitors = APIMonitor.objects.all()
                
                for monitor in api_monitors:
                    if monitor.last_notified != None and monitor.last_notified > timezone.now() - timedelta(minutes=5):
                        continue

                    alerts_config, _ = AlertsConfiguration.objects.get_or_create(team=monitor.team)
                    success_rate,_,_ = self.get_success_rate(monitor)

                    if success_rate < alerts_config.threshold_pct:
                        self.put_monitor_id_into_queue(monitor.id)
                        monitor.last_notified = timezone.now()
                        monitor.save()
                    
                # Add delay before next check
                mock_cron_interrupt()
                next_run = last_run + timedelta(seconds=cron_interval) 
                sleep_duration = (next_run - timezone.now()).total_seconds()
                time.sleep(max(sleep_duration, 0))  
        except BaseException as e:
            # Gracefully shutdown thread worker
            for channel in self.channels:
                q = self.queue[channel]
                q.join()
            
            self.stop_signal.set()
            for thread in thread_pool:
                thread.join()            
            raise e
