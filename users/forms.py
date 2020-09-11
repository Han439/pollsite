from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import MyUser

from django import forms
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):

	class Meta(UserCreationForm):
		model = MyUser
		fields = ['email', 'first_name', 'last_name']

class CustomUserChangeForm(UserChangeForm):

	class Meta:
		model = MyUser
		fields = ['email']