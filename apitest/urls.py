from django.urls import path

from apitest import views

urlpatterns = [
    path('', views.APITestView.as_view(),  name='api-test'),
]
