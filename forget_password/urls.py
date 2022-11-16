from django.urls import path

from forget_password.views import RequestForgetPasswordTokenView, ResetPasswordView


urlpatterns = [
    path('token/', RequestForgetPasswordTokenView.as_view(), name='reset-password-token'),
    path('change/', ResetPasswordView.as_view(), name='reset-password'),
]
