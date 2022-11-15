from django.contrib import admin
from login.models import MonAPIToken, Team, TeamMember

admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(MonAPIToken)
