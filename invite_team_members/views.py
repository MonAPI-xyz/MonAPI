from datetime import timedelta
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import views, status
from rest_framework.response import Response

from invite_team_members.models import InviteTeamMemberToken
from invite_team_members.serializers import InviteTeamMemberTokenCheckSerializer

import os


class RequestInviteTeamMemberTokenView(views.APIView):
    pass