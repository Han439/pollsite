from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import MyUser
from django.utils import timezone


# Create your models here.

class Tag(models.Model):
	tag = models.CharField(max_length=50, default="")

	def __str__(self):
		return self.tag

class PollQuestion(models.Model):
	question = models.CharField(max_length=250,null=True)
	user = models.ForeignKey(MyUser, null=True,on_delete=models.SET_NULL)
	tag = models.ManyToManyField(Tag, blank=True)

	def __str__(self):
		return self.question

	def get_absolute_url(self):
		"""Returns the url to access a particular instance of the model."""
		return reverse('poll_detail', args=[str(self.id)])  # reverse the url mapping from name --> view --> url

class PollOption(models.Model):
	question = models.ForeignKey(PollQuestion, on_delete=models.CASCADE)
	option = models.TextField(null=True)
	vote = models.IntegerField(default=0)

	def __str__(self):
		return self.option

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