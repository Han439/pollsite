from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.contrib.auth import get_user_model

from ..models import PollQuestion, PollOption, VoteEntry

# Create your tests here.


class TestPollQuestionModel(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            email='test@gmail.com', password='12345678')
        self.question1 = PollQuestion.objects.create(
            question='Question 1!', user=self.test_user)
        self.option1 = PollOption.objects.create(
            question=self.question1, option='yess', vote=15)
        self.option2 = PollOption.objects.create(
            question=self.question1, option='option', vote=5)

    def test_poll_question_slug_assigned_on_saved(self):
        self.assertEqual(self.question1.slug, 'question-1')

    def test_poll_question_get_total_vote(self):
        self.assertEqual(self.question1.get_total_vote(), 20)

    def test_poll_question_get_total_vote_with_no_option(self):
        question2 = PollQuestion.objects.create(
            question='no option', user=self.test_user)

        self.assertEqual(question2.get_total_vote(), 0)

    def test_poll_question_get_total_vote_with_no_vote(self):
        question3 = PollQuestion.objects.create(
            question='no vote', user=self.test_user)
        option_no_vote = PollOption.objects.create(
            question=question3, option='test', vote=0)

        self.assertEqual(question3.get_total_vote(), 0)


class TestModels(TestCase):

    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            email='test@gmail.com', password='12345678')
        self.question1 = PollQuestion.objects.create(
            question='Question 1!', user=self.test_user)
        self.option1 = PollOption.objects.create(
            question=self.question1, option='yess', vote=15)
        self.option2 = PollOption.objects.create(
            question=self.question1, option='option', vote=5)

    def test_poll_option_percentage(self):
        self.assertEqual(self.option1.get_percentage(), 75)
        self.assertEqual(self.option2.get_percentage(), 25)
