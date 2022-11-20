from django.urls import path

from invite_team_members.views import RequestInviteTeamMemberTokenView, AcceptInviteView, CancelInviteView

urlpatterns=[
    path('token/', RequestInviteTeamMemberTokenView.as_view(), name='invite-member-token'),
    path('accept/', AcceptInviteView.as_view(), name='accept-invite'),
    path('cancel/', CancelInviteView.as_view(), name='cancel-invite'),
]