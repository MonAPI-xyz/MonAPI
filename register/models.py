from django.db import models
from django.contrib.auth.models import User
import uuid


class VerifiedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)


class VerifiedUserToken(models.Model):
    verified_user = models.ForeignKey(VerifiedUser, on_delete=models.CASCADE)
    key = models.CharField(max_length=256, default=uuid.uuid4)
