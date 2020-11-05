import json
import time

from django.test import TestCase
from django.test import TestCase, SimpleTestCase, Client
from django.urls import resolve, reverse
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework.test import APIClient

from .. import views
from ..models import PollQuestion, PollOption, VoteEntry
from ..forms import PollQuestionForm
from ..serializers import PollOptionSerializer

# Create your tests here.


class TestPollView(TestCase):

    def setUp(self):
        self.poll_url = reverse('all_poll')
        self.test_user = get_user_model().objects.create_user(
            email='test@gmail.com', password='secret')
        self.poll1 = PollQuestion.objects.create(
            question='poll 1', user=self.test_user)
        self.poll2 = PollQuestion.objects.create(
            question='poll 2', user=self.test_user)

    def test_poll_GET(self):
        response = self.client.get(self.poll_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/poll.html')
        self.assertContains(response, 'poll 1')
        self.assertContains(response, 'poll 2')


class TestPollCreateView(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            email='test@gmail.com', password='secret')
        self.create_poll_url = reverse('create_poll')

    def test_create_poll_GET_without_authentication(self):
        response = self.client.get(self.create_poll_url)
        self.assertEqual(response.status_code, 302)

    def test_create_poll_GET_with_authentication(self):
        c = Client()
        c.force_login(user=self.test_user)
        response = c.get(self.create_poll_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/poll_create.html')

    def test_create_poll_POST_without_login(self):
        response = self.client.post(self.create_poll_url, {'form-TOTAL_FORMS': 1,
                                                           'form-INITIAL_FORMS': 0,
                                                           'question': 'some question ?', 'form-0-option': 'option 1', 'form-1-option': 'some option'})

        self.assertEqual(response.status_code, 302)

    def test_create_poll_POST_with_authentication(self):
        c = Client()
        c.force_login(user=self.test_user)
        response = c.post(self.create_poll_url, {'form-TOTAL_FORMS': 2,
                                                 'form-INITIAL_FORMS': 0,
                                                 'question': 'some question ?', 'form-0-option': 'option 1', 'form-1-option': 'some option'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(PollQuestion.objects.count(), 1)
        self.assertEqual(PollOption.objects.count(), 2)

    def test_create_poll_POST_with_invalid_data(self):
        c = Client()
        c.force_login(user=self.test_user)
        response = c.post(self.create_poll_url, {'form-TOTAL_FORMS': 2,
                                                 'form-INITIAL_FORMS': 0, 'form-0-option': 'option 1', 'form-1-option': 'some option'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/poll_create.html')


class TestPollDetailView(TestCase):

    def setUp(self):
        self.owner = get_user_model().objects.create_user(
            email='test1@gmail.com', password='secret')
        self.auth_user = get_user_model().objects.create_user(
            email='test2@gmail.com', password='secret')
        self.question = PollQuestion.objects.create(
            question='question detail', user=self.owner)
        self.option1 = PollOption.objects.create(
            question=self.question, option='option 1', vote=0)

        self.poll_detail_url = reverse('poll_detail', kwargs={
                                       'pk': self.question.id, 'question': self.question.slug})
        self.login_url = reverse(settings.LOGIN_URL)

    def test_poll_detail_view_without_login(self):
        response = self.client.get(self.poll_detail_url, follow=True)

        redirect_link = response.redirect_chain[0][0]
        redirect_status_code = response.redirect_chain[0][1]

        self.assertEqual(redirect_status_code, 302)
        self.assertEqual(redirect_link, ''.join(
            [self.login_url, '?next=', self.poll_detail_url]))

    def test_poll_detail_poll_owner_user_login(self):
        c = Client()
        c.force_login(user=self.owner)
        response = c.get(self.poll_detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/poll_result.html')
        self.assertContains(response, 'question detail')

    def test_poll_detail_user_without_vote_entry(self):
        c = Client()
        c.force_login(user=self.auth_user)
        response = c.get(self.poll_detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/poll_detail.html')
        self.assertContains(response, 'question detail')

    def test_poll_detail_user_with_vote_entry(self):
        user_vote_entry = VoteEntry.objects.create(
            question=self.question, voted_option=self.option1, user=self.auth_user)
        c = Client()
        c.force_login(user=self.auth_user)
        response = c.get(self.poll_detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/poll_result.html')
        self.assertContains(response, 'question detail')

    def test_poll_detail_closed_poll(self):
        closed_poll = PollQuestion.objects.create(
            question='Closed poll', user=self.owner, close=True)

        c = Client()
        c.force_login(user=self.auth_user)
        response = c.get(reverse('poll_detail', kwargs={
                         'pk': closed_poll.id, 'question': closed_poll.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/poll_result.html')

    def test_poll_detail_with_invalid_poll(self):
        c = Client()
        c.force_login(user=self.auth_user)
        response = c.get(reverse('poll_detail', kwargs={
                         'pk': 1000, 'question': 'some-slug'}))

        self.assertEqual(response.status_code, 404)


class TestProfileView(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            email='test@gmail.com', password='secret')
        self.profile_url = reverse('profile')
        self.login_url = reverse(settings.LOGIN_URL)

    def test_profile_with_authentication(self):
        c = Client()
        c.force_login(user=self.test_user)
        response = c.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/profile.html')

    def test_profile_without_authentication(self):
        response = self.client.get(self.profile_url, follow=True)

        redirect_link = response.redirect_chain[0][0]
        redirect_status_code = response.redirect_chain[0][1]
        self.assertEqual(redirect_status_code, 302)
        self.assertEqual(redirect_link, ''.join(
            [self.login_url, '?next=', self.profile_url]))

    def test_profile_user_poll(self):
        PollQuestion.objects.create(question='poll 1', user=self.test_user)
        PollQuestion.objects.create(question='poll 2', user=self.test_user)
        c = Client()
        c.force_login(user=self.test_user)
        response = c.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'poll 1')
        self.assertContains(response, 'poll 2')


class TestEditProfileView(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            email='test@gmail.com', password='secret')
        self.login_url = reverse(settings.LOGIN_URL)
        self.profile_url = reverse('profile')
        self.edit_profile_url = reverse('edit_profile')

    def test_edit_profile_GET_request(self):
        c = Client()
        c.force_login(user=self.test_user)
        response = c.get(self.edit_profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/edit_profile.html')

    def test_edit_profile_GET_request_without_authentication(self):
        response = self.client.get(self.edit_profile_url, follow=True)

        redirect_link = response.redirect_chain[0][0]
        redirect_status_code = response.redirect_chain[0][1]

        self.assertEqual(redirect_status_code, 302)
        self.assertEqual(redirect_link, ''.join(
            [self.login_url, '?next=', self.edit_profile_url]))

    def test_edit_profile_POST_request(self):
        c = Client()
        c.force_login(user=self.test_user)
        response = c.post(self.edit_profile_url, {
                          'first_name': 'Loki', 'last_name': 'Thompson'}, follow=True)

        redirect_link = response.redirect_chain[0][0]
        redirect_status_code = response.redirect_chain[0][1]

        self.assertEqual(redirect_status_code, 302)
        self.assertEqual(redirect_link, self.profile_url)
        self.assertContains(response, 'Loki')
        self.assertContains(response, 'Thompson')

    def test_edit_profile_POST_request_without_login(self):
        response = self.client.post(self.edit_profile_url, {
            'first_name': 'Loki', 'last_name': 'Thompson'}, follow=True)

        redirect_link = response.redirect_chain[0][0]
        redirect_status_code = response.redirect_chain[0][1]

        self.assertEqual(redirect_status_code, 302)
        self.assertEqual(redirect_link, ''.join(
            [self.login_url, '?next=', self.edit_profile_url]))


class TestPollDetailAPI(TestCase):

    def setUp(self):
        self.owner = get_user_model().objects.create_user(
            email='test1@gmail.com', password='secret')
        self.auth_user = get_user_model().objects.create_user(
            email='test2@gmail.com', password='secret')
        self.question = PollQuestion.objects.create(
            question='detail question', user=self.owner)
        self.option1 = PollOption.objects.create(
            question=self.question, option='option 1', vote=0)
        self.option2 = PollOption.objects.create(
            question=self.question, option='option 2', vote=1)
        self.url = reverse('api_poll_detail', kwargs={
                           'question': self.question.id})

    def test_poll_detail_API_GET_without_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_poll_detail_API_GET_with_authentication(self):
        c = APIClient()
        c.force_login(user=self.auth_user)
        response = c.get(self.url)
        poll_option = PollOption.objects.filter(question=self.question)
        serializer = PollOptionSerializer(poll_option, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_poll_detail_API_GET_with_invalid_question(self):
        c = APIClient()
        c.force_login(user=self.auth_user)
        response = c.get(
            reverse('api_poll_detail', kwargs={'question': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_poll_detail_API_GET_with_empty_options_poll(self):
        empty_poll = PollQuestion.objects.create(
            question='empty poll', user=self.owner)
        c = APIClient()
        c.force_login(user=self.auth_user)
        response = c.get(
            reverse('api_poll_detail', kwargs={'question': empty_poll.id}), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_poll_detail_API_PUT_with_invalid_question(self):
        c = APIClient()
        c.force_login(user=self.auth_user)
        response = c.put(
            reverse('api_poll_detail', kwargs={'question': 1000}), json.dumps({'id': 2}), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_poll_detail_API_PUT_with_invalid_data(self):
        c = APIClient()
        c.force_login(user=self.auth_user)
        response = c.put(self.url, json.dumps(
            {'id': 1000}), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_poll_detail_API_PUT_without_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_poll_detail_API_PUT_without_vote_entry(self):
        voted_option = PollOption.objects.create(
            question=self.question, option='option voted', vote=1)
        c = APIClient()
        c.force_login(user=self.auth_user)
        payload = {'id': voted_option.id}
        response = c.put(self.url, json.dumps(payload),
                         content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(PollOption.objects.get(pk=voted_option.id).vote, 2)
        self.assertIn('success', response.data)

    def test_poll_detail_API_PUT_with_vote_entry(self):
        voted_option = PollOption.objects.create(
            question=self.question, option='option voted', vote=1)
        vote_entry = VoteEntry.objects.create(
            question=self.question, voted_option=voted_option, user=self.auth_user)
        c = APIClient()
        c.force_login(user=self.auth_user)
        payload = json.dumps({'id': voted_option.id})
        response = c.put(self.url, payload, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(PollOption.objects.get(pk=voted_option.id).vote, 1)
        self.assertIn('error', response.data)

    def test_poll_detail_API_PUT_with_owner_user(self):
        voted_option = PollOption.objects.create(
            question=self.question, option='option voted', vote=1)
        c = APIClient()
        c.force_login(user=self.owner)
        payload = json.dumps({'id': voted_option.id})
        response = c.put(self.url, payload, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(PollOption.objects.get(pk=voted_option.id).vote, 1)
        self.assertIn('error', response.data)


class TestPollQuestionAPI(TestCase):

    def setUp(self):
        self.owner = get_user_model().objects.create_user(
            email='test1@gmail.com', password='secret')
        self.auth_user = get_user_model().objects.create_user(
            email='test2@gmail.com', password='secret')
        self.question = PollQuestion.objects.create(
            question='detail question', user=self.owner)
        self.url = reverse('api_poll', kwargs={'question': self.question.id})
        self.payload = json.dumps({'close': True})

    def test_poll_question_API_PUT_without_authentication(self):
        response = self.client.put(
            self.url, self.payload, content_type='application/json')

        self.assertEqual(response.status_code, 302)

    def test_poll_question_API_PUT_with_owner_user(self):
        c = APIClient()
        c.force_login(user=self.owner)
        response = c.put(self.url, self.payload,
                         content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(PollQuestion.objects.get(
            pk=self.question.id).close, True)

    def test_poll_question_API_PUT_without_owner_user(self):
        c = APIClient()
        c.force_login(user=self.auth_user)
        response = c.put(self.url, self.payload,
                         content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(PollQuestion.objects.get(
            pk=self.question.id).close, False)
        self.assertIn('error', response.data)

    def test_poll_question_API_PUT_with_invalid_data(self):
        c = APIClient()
        c.force_login(user=self.auth_user)
        response = c.put(self.url, {'close': 'invalid'},
                         content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(PollQuestion.objects.get(
            pk=self.question.id).close, False)

    def test_poll_question_API_DELETE_without_authentication(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 302)

    def test_poll_question_API_DELETE_with_owner_user(self):
        c = APIClient()
        c.force_login(user=self.owner)
        response = c.delete(self.url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(PollQuestion.objects.count(), 0)

    def test_poll_question_API_DELETE_without_owner_user(self):
        c = APIClient()
        c.force_login(user=self.auth_user)
        response = c.delete(self.url)

        self.assertIn('error', response.data)
        self.assertEqual(PollQuestion.objects.count(), 1)
