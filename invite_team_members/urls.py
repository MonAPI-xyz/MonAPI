from django.urls import path

from invite_team_members.views import RequestInviteTeamMemberTokenView

urlpatterns=[
    path('token/', RequestInviteTeamMemberTokenView.as_view(), name='invite-member-token')
]