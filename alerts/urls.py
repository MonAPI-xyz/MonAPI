from django.urls import path, include
from rest_framework import routers

from alerts.views import AlertConfiguration

urlpatterns = [
    path('config/', AlertConfiguration.as_view(), name='alert-configuration'),
]
