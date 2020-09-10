from rest_framework import serializers

from .models import PollOption, VoteEntry

class PollOptionSerializer(serializers.ModelSerializer):

	class Meta:
		model = PollOption
		fields = ['id', 'question', 'option', 'vote']

class VoteEntrySerializer(serializers.ModelSerializer):

	class Meta:
		model = VoteEntry
		fields = ['id', 'question', 'voted_option', 'user']