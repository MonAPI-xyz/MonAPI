from rest_framework.authtoken.models import Token
from login.models import MonAPIToken, TeamMember

def generate_token(user):
    team_member_query = TeamMember.objects.filter(user=user)
    
    if not team_member_query.exists():
        team_member = TeamMember.objects.create(user=user)
    else:
        team_member = team_member_query.first()
        
    token = MonAPIToken.objects.create(team_member=team_member)
    return token.key