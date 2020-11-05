from django import forms
from .models import PollOption, PollQuestion


class PollQuestionForm(forms.ModelForm):

    class Meta:
        model = PollQuestion
        fields = ['question']
