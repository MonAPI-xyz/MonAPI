from django.contrib import admin

from apimonitor.models import APIMonitor, APIMonitorBodyForm, APIMonitorRawBody, APIMonitorHeader, APIMonitorQueryParam, APIMonitorResult, AssertionExcludeKey, AlertsConfiguration


admin.site.register(APIMonitor)
admin.site.register(APIMonitorBodyForm)
admin.site.register(APIMonitorRawBody)
admin.site.register(APIMonitorHeader)
admin.site.register(APIMonitorQueryParam)
admin.site.register(APIMonitorResult)
admin.site.register(AssertionExcludeKey)
admin.site.register(AlertsConfiguration)
