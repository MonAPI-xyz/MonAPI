from django.db import models
from django.contrib.auth.models import User

import binascii
import os

class Team(models.Model):
    name = models.CharField(max_length=128)
    
class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('team', 'user',)
    
class MonAPIToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    team_member = models.ForeignKey(TeamMember, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)
    
    @property
    def team(self):
        return self.team_member.team

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key
    