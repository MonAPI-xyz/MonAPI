from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.urls import reverse

from login.models import MonAPIToken, Team, TeamMember

# Create your tests here.
class APITest(APITestCase):
    #GET
    def test_api_test_get(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'method': 'GET',
            'url': 'https://google.com',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
       

        # Expected JSON from frontend
        received_json = {
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
        }

        # Get path
        api_test_path = reverse('api-test')
        response = self.client.post(api_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_test_get_wrong_url(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'method': 'GET',
            'url': 'abcdefg',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
       

        # Expected JSON from frontend
        received_json = {
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
        }

        # Get path
        api_test_path = reverse('api-test')
        response = self.client.post(api_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_test_get_query_param_failed(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'method': 'GET',
            'url': 'https://google.com',
        }

        queryparam_value = [
            {
                'value': 'value1',
                'corrupted': 'corrupted'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
       

        # Expected JSON from frontend
        received_json = {
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
        }

        # Get path
        api_test_path = reverse('api-test')
        response = self.client.post(api_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_test_get_query_param_failed_none(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'method': 'GET',
            'url': 'https://google.com',
        }

        queryparam_value = [
            {
                'key': None,
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
       

        # Expected JSON from frontend
        received_json = {
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
        }

        # Get path
        api_test_path = reverse('api-test')
        response = self.client.post(api_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_test_get_headers_failed(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'method': 'GET',
            'url': 'https://google.com',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'value': 'value1',
            'corrupted': 'corrupted'
        }]
       

        # Expected JSON from frontend
        received_json = {
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
        }

        # Get path
        api_test_path = reverse('api-test')
        response = self.client.post(api_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_test_get_headers_failed_none(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'method': 'GET',
            'url': 'https://google.com',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key1',
            'value': None
        }]
       

        # Expected JSON from frontend
        received_json = {
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
        }

        # Get path
        api_test_path = reverse('api-test')
        response = self.client.post(api_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    #POST    
    def test_api_test_post_no_body(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'method': 'POST',
            'url': 'https://google.com',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
       

        # Expected JSON from frontend
        received_json = {
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
        }

        # Get path
        api_test_path = reverse('api-test')
        response = self.client.post(api_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_api_test_post_form(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'method': 'POST',
            'url': 'https://google.com',
            'body_type': 'FORM',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
        monitorbodyform_value = [
            {
                'key': 'key4',
                'value': 'value4'
            },
            {
                'key': 'key5',
                'value': 'value5'
            }
        ]
        monitorrawbody_value = "This doesn't matter since body type is FORM"

        # Expected JSON from frontend
        received_json = {
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'body_type' : monitor_value['body_type'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value
        }

        # Get path
        api_test_path = reverse('api-test')
        response = self.client.post(api_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_test_post_form_failed(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'method': 'POST',
            'url': 'https://api-staging.monapi.xyz/',
            'body_type': 'FORM',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
        monitorbodyform_value = [
            {
                'value': 'value1',
                'corrupted': 'corrupted'
            }
        ]
        monitorrawbody_value = "This doesn't matter since body type is FORM"

        # Expected JSON from frontend
        received_json = {
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'body_type' : monitor_value['body_type'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value
        }

        # Get path
        api_test_path = reverse('api-test')
        response = self.client.post(api_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_test_post_form_failed_none(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'method': 'POST',
            'url': 'https://api-staging.monapi.xyz/',
            'body_type': 'FORM',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
        monitorbodyform_value = [
            {
                'key': 'key3',
                'value': None
            }
        ]
        monitorrawbody_value = "This doesn't matter since body type is FORM"

        # Expected JSON from frontend
        received_json = {
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'body_type' : monitor_value['body_type'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value
        }

        # Get path
        api_test_path = reverse('api-test')
        response = self.client.post(api_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_test_post_raw_body(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'method': 'POST',
            'url': 'https://google.com',
            'body_type': 'RAW',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
        monitorbodyform_value = "This doesn't matter since body type is RAW"
        monitorrawbody_value = "Valid raw body"

        # Expected JSON from frontend
        received_json = {
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'body_type' : monitor_value['body_type'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value
        }

        # Get path
        api_test_path = reverse('api-test')
        response = self.client.post(api_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    #PATCH    
    def test_api_test_patch_no_body(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'method': 'PATCH',
            'url': 'https://google.com',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
       

        # Expected JSON from frontend
        received_json = {
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
        }

        # Get path
        api_test_path = reverse('api-test')
        response = self.client.post(api_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_api_test_patch_form(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'method': 'PATCH',
            'url': 'https://google.com',
            'body_type': 'FORM',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
        monitorbodyform_value = [
            {
                'key': 'key4',
                'value': 'value4'
            },
            {
                'key': 'key5',
                'value': 'value5'
            }
        ]
        monitorrawbody_value = "Valid raw body"

        # Expected JSON from frontend
        received_json = {
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'body_type' : monitor_value['body_type'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value
        }

        # Get path
        api_test_path = reverse('api-test')
        response = self.client.post(api_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_test_patch_raw_body(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'method': 'PATCH',
            'url': 'https://google.com',
            'body_type': 'RAW',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
        monitorbodyform_value = "This doesn't matter since body type is RAW"
        monitorrawbody_value = "Valid raw body"

        # Expected JSON from frontend
        received_json = {
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'body_type' : monitor_value['body_type'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value
        }

        # Get path
        api_test_path = reverse('api-test')
        response = self.client.post(api_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    #PUT   
    def test_api_test_put_no_body(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'method': 'PUT',
            'url': 'https://google.com',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
       

        # Expected JSON from frontend
        received_json = {
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
        }

        # Get path
        api_test_path = reverse('api-test')
        response = self.client.post(api_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_api_test_put_form(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'method': 'PUT',
            'url': 'https://google.com',
            'body_type': 'FORM',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
        monitorbodyform_value = [
            {
                'key': 'key4',
                'value': 'value4'
            },
            {
                'key': 'key5',
                'value': 'value5'
            }
        ]
        monitorrawbody_value = "This doesn't matter since body type is FORM"

        # Expected JSON from frontend
        received_json = {
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'body_type' : monitor_value['body_type'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value
        }

        # Get path
        api_test_path = reverse('api-test')
        response = self.client.post(api_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_test_put_raw_body(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'method': 'PUT',
            'url': 'https://google.com',
            'body_type': 'RAW',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
        monitorbodyform_value = "This doesn't matter since body type is RAW"
        monitorrawbody_value = "Valid raw body"

        # Expected JSON from frontend
        received_json = {
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'body_type' : monitor_value['body_type'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value
        }

        # Get path
        api_test_path = reverse('api-test')
        response = self.client.post(api_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    #DELETE   
    def test_api_test_delete_no_body(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'method': 'DELETE',
            'url': 'https://google.com',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
       

        # Expected JSON from frontend
        received_json = {
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
        }

        # Get path
        api_test_path = reverse('api-test')
        response = self.client.post(api_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_api_test_delete_form(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'method': 'DELETE',
            'url': 'https://google.com',
            'body_type': 'FORM',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
        monitorbodyform_value = [
            {
                'key': 'key4',
                'value': 'value4'
            },
            {
                'key': 'key5',
                'value': 'value5'
            }
        ]
        monitorrawbody_value = "This doesn't matter since body type is FORM"

        # Expected JSON from frontend
        received_json = {
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'body_type' : monitor_value['body_type'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value
        }

        # Get path
        api_test_path = reverse('api-test')
        response = self.client.post(api_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_test_delete_raw_body(self):
        # Create a user object
        user = User.objects.create_user(username="test@test.com", email="test@test.com", password="Test1234")
        team = Team.objects.create(name='test team')
        team_member = TeamMember.objects.create(team=team, user=user)
        
        token = MonAPIToken.objects.create(team_member=team_member)
        header = {'HTTP_AUTHORIZATION': f"Token {token.key}"}

        monitor_value = {
            'method': 'DELETE',
            'url': 'https://google.com',
            'body_type': 'RAW',
        }

        queryparam_value = [
            {
                'key': 'key1',
                'value': 'value1'
            },
            {
                'key': 'key2',
                'value': 'value2'
            }
        ]
        monitorheader_value = [{
            'key': 'key3',
            'value': 'value3'
        }]
        monitorbodyform_value = "This doesn't matter since body type is RAW"
        monitorrawbody_value = "Valid raw body"

        # Expected JSON from frontend
        received_json = {
            'method': monitor_value['method'],
            'url': monitor_value['url'],
            'body_type' : monitor_value['body_type'],
            'query_params': queryparam_value,
            'headers': monitorheader_value,
            'body_form': monitorbodyform_value,
            'raw_body': monitorrawbody_value
        }

        # Get path
        api_test_path = reverse('api-test')
        response = self.client.post(api_test_path, data=received_json, format='json', **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

























