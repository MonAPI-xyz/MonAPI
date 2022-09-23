from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class APIViewTestCase(APITestCase):
    def test_user_can_register(self):
        response = self.client.post(
            reverse('register-api'),
            {
                'email': 'user1@gmail.com',
                'password': 'Abcd1234',
                'password2': 'Abcd1234'
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

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

        self.assertEqual(response.data['password'][0].title(),
                         str(['This Password Is Too Short. It Must Contain At Least 8 Characters.',
                              'This Password Is Too Common.',
                              'The Password Must Contain At Least 1 Digit, 0-9.',
                              'The Password Must Contain At Least 1 Uppercase Letter, A-Z.'])
                         )