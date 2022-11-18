import pytz

from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import datetime

from invite_team_members.models import InviteTeamMemberToken
# Create your tests here.
class InviteTeamMemberTokenTest(TestCase):
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    mock_current_time = local_timezone.localize(datetime(2022, 9, 20, 10))

    def setUp(self):
        timezone.now = lambda: self.mock_current_time

    def test_when_created_key_is_made(self):
        user = User.objects.create_user(username='test@gmail.com', email='test@gmail.com', password='Test1234')
        inviteToken =  InviteTeamMemberToken.objects.create(user=user)
        self.assertEqual(InviteTeamMemberToken.objects.all().count(), 1)
