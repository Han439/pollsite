from rest_framework import serializers

from .models import PollOption, VoteEntry, PollQuestion


class PollQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PollQuestion
        read_only_fields = ['id', 'question', 'user']
        fields = ['id', 'question', 'user', 'close']


class PollOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PollOption
        read_only_fields = ['question', 'option', 'vote']
        fields = ['id', 'question', 'option', 'vote']


class VoteEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = VoteEntry
        fields = ['id', 'question', 'voted_option', 'user']
