from django.test import SimpleTestCase
from django.urls import resolve, reverse

from .. import views


# Create your tests here.


class TestUrls(SimpleTestCase):

    def test_all_poll_url_resolve(self):
        url = reverse('all_poll')
        self.assertEqual(resolve(url).func, views.poll)

    def test_create_poll_url_resolve(self):
        url = reverse('create_poll')
        self.assertEqual(resolve(url).func, views.create_poll)

    def test_poll_detail_url_resolve(self):
        url = reverse('poll_detail', kwargs={
                      'pk': 1, 'question': 'slug-question'})
        self.assertEqual(resolve(url).func, views.poll_detail)

    def test_profile_url_resolve(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func, views.profile)

    def test_edit_profile_url_resolve(self):
        url = reverse('edit_profile')
        self.assertEqual(resolve(url).func, views.edit_profile)

    def test_api_poll_detail_url_resolve(self):
        url = reverse('api_poll_detail', kwargs={'question': 2})
        self.assertEqual(resolve(url).func.view_class, views.PollDetailAPI)

    def test_api_poll_url_resolve(self):
        url = reverse('api_poll', kwargs={'question': 3})
        self.assertEqual(resolve(url).func.view_class, views.PollQuestionAPI)
