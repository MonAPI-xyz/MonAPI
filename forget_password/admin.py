from django.contrib import admin
from forget_password.models import ForgetPasswordToken

admin.site.register(ForgetPasswordToken)
