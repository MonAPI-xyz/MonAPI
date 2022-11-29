from django.contrib import admin

from statuspage.models import StatusPageCategory, StatusPageConfiguration

admin.site.register(StatusPageConfiguration)
admin.site.register(StatusPageCategory)
