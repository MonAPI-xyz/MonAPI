from django.urls import path
from register.views import registration_view

urlpatterns = [
    path('api', registration_view, name='register-api')
]