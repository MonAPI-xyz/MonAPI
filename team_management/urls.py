from django.urls import path, include
from team_management import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', views.TeamManagementViewSet, basename='team-management')
urlpatterns = [
    path('', include(router.urls)),
]
