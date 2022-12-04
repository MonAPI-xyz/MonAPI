from django.urls import path
from register.views import registration_view, verify_view

urlpatterns = [
    path('api', registration_view, name='register-api'),
    path('verify', verify_view, name='verify-user')
]