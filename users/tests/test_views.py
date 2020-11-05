from django.urls import resolve, reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import TestCase

from rest_framework.test import APIClient

from .. import views
from ..serializers import UserSerializer

# Create your tests here.


class TestRegistrationView(TestCase):

    def setUp(self):
        self.url = reverse('registration')

    def test_registration_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_registration_POST_with_valid_payload(self):
        payload = {
            'email': 'valid@gmail.com',
            'first_name': 'tom',
            'last_name': 'sona',
            'password1': 'password',
            'password2': 'password'
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_registration_POST_with_valid_payload(self):
        payload = {
            'email': 'validgmail',
            'first_name': 'tom',
            'last_name': 'sona',
            'password1': 'passwo',
            'password2': 'password'
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/registration.html')
        self.assertEqual(get_user_model().objects.count(), 0)


class TestUserAPIView(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create(
            email='test@gmail.com', password='word')
        self.url = reverse('user-api')

    def test_user_API_GET(self):
        response = self.client.get(self.url)
        users = get_user_model().objects.all()
        serializer = UserSerializer(users, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)
