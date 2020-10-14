from django import forms
from .models import PollOption, PollQuestion
from django.contrib.auth.models import User


class PollForm(forms.Form):
	option = forms.CharField(max_length=300)

class PollQuestionForm(forms.ModelForm):

	class Meta:
		model = PollQuestion
		fields = ['question']

class UserForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('first_name', 'last_name')


