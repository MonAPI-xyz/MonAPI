from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from login.models import Team, TeamMember, MonAPIToken

class TeamManagementTests(APITestCase):
  url = reverse('team-management-list')
  test_url = reverse('team-management-current')

  def test_when_non_authenticated_then_return_unauthorized(self):
    new_team_request = {
      "name": "test team",
      "description": "test description",
      "logo": "testLogo.png",
    }

    response = self.client.post(self.url, data=new_team_request, format='json')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertEqual(response.data, {
        "detail": "Authentication credentials were not provided."
    })

  def test_when_authenticated_and_empty_team_name_then_return_bad_request(self):
    user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
    team = Team.objects.create(name='myteam')
    team_member = TeamMember.objects.create(team=team, user=user)
    
    token = MonAPIToken.objects.create(team_member=team_member)
    header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

    new_team_request = {
      "name": "",
    }

    response = self.client.post(self.url, data=new_team_request, format='json', **header)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data, {
        "error": "Please make sure your [team name] is exist!"
    })

  def test_when_authenticated_and_not_empty_team_name_then_return_success(self):
    user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
    team = Team.objects.create(name='myteam')
    team_member = TeamMember.objects.create(team=team, user=user)
    
    token = MonAPIToken.objects.create(team_member=team_member)
    header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

    new_team_request = {
      "name": "test team",
    }

    response = self.client.post(self.url, data=new_team_request, format='json', **header)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['name'], "test team")

  def test_when_authenticated_and_complete_team_data_then_return_success(self):
    user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
    team = Team.objects.create(name='myteam')
    team_member = TeamMember.objects.create(team=team, user=user)
    
    token = MonAPIToken.objects.create(team_member=team_member)
    header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

    new_team_request = {
      "name": "test team",
      "description": "test description",
      "logo": "testLogo.png",
    }

    response = self.client.post(self.url, data=new_team_request, format='json', **header)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['name'], "test team")
  
  def test_retrieve(self):
    user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
    team = Team.objects.create(name='myteam')
    team_member = TeamMember.objects.create(team=team, user=user)

    token = MonAPIToken.objects.create(team_member=team_member)
    header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
    
    response = self.client.get(self.test_url, format='json', **header)
    self.assertEqual(response.data,{'id': 1, 'name': 'myteam', 'logo': None, 'description': '', 'teammember': [1]})

    





  