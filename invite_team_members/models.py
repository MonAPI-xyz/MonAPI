import uuid
from django.db import models
from django.contrib.auth.models import User
from login.models import TeamMember

class InviteTeamMemberToken(models.Model):
    team_member = models.ForeignKey(TeamMember, on_delete=models.CASCADE)
    key = models.CharField(max_length=256, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
