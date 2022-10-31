from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class ThresholdConfig(models.Model):
    time_window_choices = [
        ('1H',  '1 Hour' ),
        ('2H',  '2 Hour' ),
        ('3H',  '3 Hour' ),
        ('6H',  '6 Hour' ),
        ('12H', '12 Hour'),
        ('24H', '24 Hour')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    threshold_pct = models.IntegerField(null=True, blank=True, default=100, validators=[
        MinValueValidator(1),
        MaxValueValidator(100)
    ])
    time_window = models.CharField(max_length=16, choices=time_window_choices, default='1H')
