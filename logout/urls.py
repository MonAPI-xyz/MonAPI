from django.urls import path
from logout import views

urlpatterns = [
    path('', views.user_logout, name='logout')
]