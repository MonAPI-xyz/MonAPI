from django.urls import path

from invite_team_members.views import RequestInviteTeamMemberTokenView, AcceptInviteView

urlpatterns=[
    path('token/', RequestInviteTeamMemberTokenView.as_view(), name='invite-member-token'),
    path('accept/', AcceptInviteView.as_view(), name='accept-invite'),
]