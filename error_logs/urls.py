from django.urls import path, include
from error_logs import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', views.ErrorLogsViewSet, basename='error-logs')
urlpatterns = [
    path('', include(router.urls)),
]
