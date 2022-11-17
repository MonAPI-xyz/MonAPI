"""monapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('register/', include('register.urls')),
    path('forget-password/', include('forget_password.urls')),
    path('logout/', include('logout.urls')),
    path('monitor/', include('apimonitor.urls')),
    path('auth/', include('login.urls')), # New endpoint for authentication
    path('login/', include('login.urls')),
    path('error-logs/', include('error_logs.urls')),
    path('alerts/', include('alerts.urls')),
    path('api-test/', include('apitest.urls')),
    path('team-management/', include('team_management.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
