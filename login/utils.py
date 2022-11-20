from login.models import MonAPIToken, TeamMember, Team

def generate_token(user):
    team_member_query = TeamMember.objects.filter(user=user)
    
    if not team_member_query.exists():
        username = user.username.split('@')[0]
        team = Team.objects.create(name=username.title())
        team_member = TeamMember.objects.create(user=user, team=team, verified=True)
    else:
        team_member = team_member_query.first()
        
    token = MonAPIToken.objects.create(team_member=team_member)
    return token.key