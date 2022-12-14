import os
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from login.models import Team, TeamMember, MonAPIToken
from django.core.files.uploadedfile import SimpleUploadedFile

class TeamManagementTests(APITestCase):
  list_url = reverse('team-management-list')
  current_url = reverse('team-management-current')

  def test_when_non_authenticated_then_return_unauthorized(self):
    new_team_request = {
      "name": "test team",
      "description": "test description",
      "logo": "testLogo.png",
    }

    response = self.client.post(self.list_url, data=new_team_request, format='json')
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

    response = self.client.post(self.list_url, data=new_team_request, format='json', **header)
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

    response = self.client.post(self.list_url, data=new_team_request, format='json', **header)
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

    response = self.client.post(self.list_url, data=new_team_request, format='json', **header)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.data['name'], "test team")

  def test_when_authenticated_and_update_with_not_empty_team_name_then_return_bad_request(self):
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
    target_team_id = TeamMember.objects.filter(team=team)[:1].get().id
    edit_team_url = reverse('team-management-detail', kwargs={'pk': target_team_id})    
    response = self.client.put(edit_team_url, data=new_team_request, format='json', **header)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data, {
        "error": "Team name cannot be changed!"
    })

  def test_when_authenticated_and_update_with_required_team_data_then_return_success(self):
    user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
    team = Team.objects.create(name='myteam')
    team_member = TeamMember.objects.create(team=team, user=user)
    
    token = MonAPIToken.objects.create(team_member=team_member)
    header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

    new_team_request = {
      "description": "test description",
      "logo": "testLogo.png",
    }    
    
    target_team_id = TeamMember.objects.filter(team=team)[:1].get().id
    edit_team_url = reverse('team-management-detail', kwargs={'pk': target_team_id})    
    response = self.client.put(edit_team_url, data=new_team_request, format='json', **header)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['name'], "myteam")

  
  def test_when_authenticated_and_update_with_new_image_then_return_success(self):
    
    image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
    new_image = SimpleUploadedFile(name='test_new_image.jpg', content=b'', content_type='image/jpeg')

    user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
    team = Team.objects.create(name='myteam', description='123', logo=image)
    team_logo_path = team.logo.path

    team_member = TeamMember.objects.create(team=team, user=user)
    
    token = MonAPIToken.objects.create(team_member=team_member)
    header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

    new_team_request = {
      "description": "test description",
      "logo": new_image,
    }    
    
    target_team_id = TeamMember.objects.filter(team=team)[:1].get().id
    edit_team_url = reverse('team-management-detail', kwargs={'pk': target_team_id})    
    response = self.client.put(edit_team_url, data=new_team_request, format='json', **header)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['name'], "myteam")
    self.assertEqual(os.path.exists(team_logo_path), False )

  def test_when_authenticated_and_update_only_description_then_return_success(self):
    
    image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')

    user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
    team = Team.objects.create(name='myteam', description='123', logo=image)
    team_logo_path = team.logo.path

    team_member = TeamMember.objects.create(team=team, user=user)
    
    token = MonAPIToken.objects.create(team_member=team_member)
    header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

    new_team_request = {
      "description": "test description",
    }    
    
    target_team_id = TeamMember.objects.filter(team=team)[:1].get().id
    edit_team_url = reverse('team-management-detail', kwargs={'pk': target_team_id})    
    response = self.client.put(edit_team_url, data=new_team_request, format='json', **header)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['name'], "myteam")
    self.assertEqual(os.path.exists(team_logo_path), True )

  def test_when_authenticated_and_not_in_current_edit_team_then_return_bad_request(self):
    
    user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
    team = Team.objects.create(name='myteam')
    team_two = Team.objects.create(name='myteam2')
    team_member = TeamMember.objects.create(team=team, user=user)
    TeamMember.objects.create(team=team_two, user=user)
    
    token = MonAPIToken.objects.create(team_member=team_member)
    header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

    new_team_request = {
      "description": "test description",
      "logo": "testLogo.png",
    }    

    target_team_id = TeamMember.objects.filter(team=team_two)[:1].get().id
    edit_team_url = reverse('team-management-detail', kwargs={'pk': target_team_id})    
    response = self.client.put(edit_team_url, data=new_team_request, format='json', **header)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data['error'], 'Team not found')
  
  def test_retrieve(self):
    user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
    team = Team.objects.create(name='myteam')
    team_member = TeamMember.objects.create(team=team, user=user)

    token = MonAPIToken.objects.create(team_member=team_member)
    header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}
    
    response = self.client.get(self.current_url, format='json', **header)
    self.assertEqual(response.data,{"id": 1, "name": "myteam", "logo": None, "description": "", "teammember": [{"team": 1, "user": {"id": 1, "username": "test@test.com", "email": "test@test.com", "first_name": "", "last_name": ""}, "verified": False}]})

    





  
