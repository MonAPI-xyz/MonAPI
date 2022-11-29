from django.db import models
from login.models import Team

class StatusPageConfiguration(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    path = models.CharField(max_length=64, blank=True)
    
class StatusPageCategory(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    