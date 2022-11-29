import pytz
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime

from rest_framework.test import APITestCase
from login.models import Team, TeamMember, MonAPIToken
from statuspage.models import StatusPageConfiguration, StatusPageCategory

class StatusPageConfigTest(APITestCase):
    test_url = reverse('statuspage-config')
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    mock_current_time = local_timezone.localize(datetime(2022, 9, 20, 10))

    def setUp(self):
        # Mock time function
        timezone.now = lambda: self.mock_current_time
        
    def test_status_page_config_get_first_time_then_return_success(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        response = self.client.get(self.test_url, format='json', **header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "path": ""
        })
        
    def test_status_page_config_get_when_exists_then_return_success(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        
        StatusPageConfiguration.objects.create(team=team, path="testpath")

        response = self.client.get(self.test_url, format='json', **header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "path": "testpath"
        })
        
    def test_status_page_config_update_then_return_success(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        
        req_body = {
            "path": "updatepath"
        }

        response = self.client.post(self.test_url, data=req_body, format='json', **header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "path": "updatepath"
        })
        
        status_config = StatusPageConfiguration.objects.get(team=team)
        self.assertEqual(status_config.path, "updatepath")
    
    def test_status_page_config_update_when_empty_param_then_return_success(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        
        req_body = {}

        response = self.client.post(self.test_url, data=req_body, format='json', **header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "path": ""
        })
        
    def test_status_page_config_update_when_invalid_param_then_return_error(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        
        req_body = {
            "path": None,
        }

        response = self.client.post(self.test_url, data=req_body, format='json', **header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {
            "path": ["This field may not be null."]
        })
        
class StatusPageCategoryTest(APITestCase):
    test_url = reverse('statuspage-category-list')
    local_timezone = pytz.timezone(settings.TIME_ZONE)
    mock_current_time = local_timezone.localize(datetime(2022, 9, 20, 10))

    def setUp(self):
        # Mock time function
        timezone.now = lambda: self.mock_current_time
        
    def test_status_page_category_get_then_return_list_category(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        
        StatusPageCategory.objects.create(team=team, name='category1')

        response = self.client.get(self.test_url, format='json', **header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'category1')
        
    def test_status_page_category_post_then_create_new_category(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        req_body = {
            "name": "abc"
        }

        response = self.client.post(self.test_url, data=req_body, format='json', **header)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], "abc")
        
        category = StatusPageCategory.objects.get(team=team)
        self.assertEqual(category.name, "abc")
        
    def test_status_page_category_post_invalid_param_then_return_error(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        req_body = {}

        response = self.client.post(self.test_url, data=req_body, format='json', **header)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {
            "name": ["This field is required."]
        })
        
    def test_status_page_category_delete_then_return_success(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
        
        status_page = StatusPageCategory.objects.create(team=team, name='categorydel')

        response = self.client.delete(reverse('statuspage-category-detail', kwargs={'pk': status_page.id}), format='json', **header)
        self.assertEqual(response.status_code, 204)
        
        count_status = StatusPageCategory.objects.filter(team=team).count()
        self.assertEqual(count_status, 0)
        
    def test_status_page_category_delete_not_exists_then_return_error(self):
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        response = self.client.delete(reverse('statuspage-category-detail', kwargs={'pk': 999}), format='json', **header)
        self.assertEqual(response.status_code, 404)
        
        