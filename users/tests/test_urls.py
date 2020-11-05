from django.test import TestCase, SimpleTestCase
from django.urls import resolve, reverse

from rest_framework.test import APIClient

from .. import views

# Create your tests here.


class TestUrls(SimpleTestCase):

    def test_registration_url_resolve(self):
        url = reverse('registration')
        self.assertEqual(resolve(url).func, views.registration)

    def test_user_api_url_resolve(self):
        url = reverse('user-api')
        self.assertEqual(resolve(url).func.view_class, views.UserAPI)
