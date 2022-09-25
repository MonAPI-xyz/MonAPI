from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User


class APIViewTestCase(APITestCase):
    def test_user_can_register(self):
        response = self.client.post(
            reverse('register-api'),
            {
                'email': 'user1@gmail.com',
                'password': 'B0tch1ng',
                'password2': 'B0tch1ng'
            },
        )
        # Check user is created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['response'], 'Successfully registered new user.')
        self.assertEqual(response.data['email'], 'user1@gmail.com')
        self.assertEqual(User.objects.all().count(), 1)

        # Check user is saved correctly
        new_user = User.objects.get_by_natural_key("user1@gmail.com")
        self.assertEqual(new_user.get_username(), "user1@gmail.com")
        self.assertEqual(new_user.check_password('B0tch1ng'), True)

    def test_user_password_must_match(self):
        response = self.client.post(
            reverse('register-api'),
            {
                'email': 'user2@gmail.com',
                'password': 'Aaaa1234',
                'password2': 'Bbbb1234'
            }
        )

        self.assertEqual(response.data['password'], 'Password must match.')
        self.assertEqual(response.status_code, 400)

    def test_user_password_must_follow_policy(self):
        response = self.client.post(
            reverse('register-api'),
            {
                'email': 'user3@gmail.com',
                'password': 'a',
                'password2': 'a'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password'][0].title(),
                         str(['This Password Is Too Short. It Must Contain At Least 8 Characters.',
                              'This Password Is Too Common.',
                              'The Password Must Contain At Least 1 Digit, 0-9.',
                              'The Password Must Contain At Least 1 Uppercase Letter, A-Z.'])
                         )

    def test_only_one_user_per_email(self):
        response1 = self.client.post(
            reverse('register-api'),
            {
                'email': 'user1@gmail.com',
                'password': 'B0tch1ng',
                'password2': 'B0tch1ng'
            },
        )

        response2 = self.client.post(
            reverse('register-api'),
            {
                'email': 'user1@gmail.com',
                'password': 'B0tch1ng',
                'password2': 'B0tch1ng'
            },
        )
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.data['response'],
                         'User already registered! Please use a different email to register.')