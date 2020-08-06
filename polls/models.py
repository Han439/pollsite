from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import MyUser
from django.utils import timezone
from django.db.models import Sum


# Create your models here.

class Tag(models.Model):
	tag = models.CharField(max_length=50, default="")

	def __str__(self):
		return self.tag

class PollQuestion(models.Model):
	question = models.CharField(max_length=250,null=True)
	user = models.ForeignKey(MyUser, null=True,on_delete=models.SET_NULL)
	tag = models.ManyToManyField(Tag, blank=True)
	date = models.DateTimeField(default=timezone.now, null=True)

	def __str__(self):
		return self.question

	def get_question(self):
		if len(self.question) > 80:
			return self.question[:81] + "..."
		else:
			return self.question

	def get_total_vote(self):
		return self.polloption_set.aggregate(Sum('vote'))['vote__sum']

	def get_time_delta(self):
		time = (timezone.now() - self.date)
		hours = time.seconds // 3600
		minute = (time.seconds // 60) % 60
		if time.days > 0:
			return str(time.days) + " days"
		elif hours > 0:
			return str(hours) + " hours"
		elif minute > 0:
			return str(minute) + " minutes"
		else:
			return str(time.seconds) + " seconds"

	def get_absolute_url(self):
		"""Returns the url to access a particular instance of the model."""
		return reverse('poll_detail', args=[str(self.id)])  # reverse the url mapping from name --> view --> url

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
	voted_option = models.ForeignKey(PollOption, on_delete=models.CASCADE)
	user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
	voted_date = models.DateTimeField(default=timezone.now)

class Comment(models.Model):
	comment = models.TextField(blank=True, null=True)
	question = models.ForeignKey(PollQuestion, on_delete=models.CASCADE	)
	user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
	date = models.DateTimeField(default=timezone.now)