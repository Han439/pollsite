from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import MyUser
from django.utils import timezone
from django.db.models import Sum


# Create your models here.


class PollQuestion(models.Model):
	question = models.CharField(max_length=250,null=True)
	user = models.ForeignKey(MyUser, null=True,on_delete=models.SET_NULL, blank=True)
	date = models.DateTimeField(default=timezone.now, null=True)
	close = models.BooleanField(default=False, null=True)

	def __str__(self):
		return self.question

	def get_question_slug(self):
		return (self.question).lower().replace(' ', '-')

	def get_total_vote(self):
		return self.polloption_set.aggregate(Sum('vote'))['vote__sum']


class PollOption(models.Model):
	question = models.ForeignKey(PollQuestion, on_delete=models.CASCADE)
	option = models.CharField(max_length=200, null=True)
	vote = models.IntegerField(default=0)

	def __str__(self):
		return self.option

	def get_percentage(self):
		total = self.question.get_total_vote()
		if total > 0:
			return round((self.vote / total) * 100, 1)
		else:
			return 0


class VoteEntry(models.Model):
	question = models.ForeignKey(PollQuestion, on_delete=models.CASCADE)
	voted_option = models.ForeignKey(PollOption, on_delete=models.CASCADE, blank=True, null=True)
	user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
	voted_date = models.DateTimeField(auto_now_add=True)
	voted_modified_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.email
