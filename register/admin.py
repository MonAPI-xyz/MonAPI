from django.contrib import admin
from register.models import VerifiedUser, VerifiedUserToken

admin.site.register(VerifiedUser)
admin.site.register(VerifiedUserToken)
