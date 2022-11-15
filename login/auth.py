from rest_framework.authentication import TokenAuthentication
from login.models import MonAPIToken
from rest_framework import exceptions

class MonAPITokenAuthentication(TokenAuthentication):
    model = MonAPIToken
    
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('team_member__user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')

        if not token.team_member.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        return (token.team_member.user, token)