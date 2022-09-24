from django.urls import path, include
from rest_framework import routers

from apimonitor import views


router = routers.DefaultRouter()
router.register(r'', views.APIMonitorViewSet, basename='api-monitor')

urlpatterns = [
    path('', include(router.urls)),
]
