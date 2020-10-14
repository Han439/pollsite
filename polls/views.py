from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import PollQuestion, PollOption, VoteEntry
from .forms import PollForm, PollQuestionForm, UserForm
from django.forms import formset_factory, modelformset_factory, inlineformset_factory

from django.http import Http404
from django.contrib.auth.decorators import login_required

from .serializers import PollOptionSerializer, PollQuestionSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



# Create your views here.

def poll(request):
	all_polls = PollQuestion.objects.all().order_by("-date")
	return render(request, 'polls/poll.html', {'all_polls': all_polls})


def poll_detail(request, pk, question):
	poll = get_object_or_404(PollQuestion, pk=pk)
	context = {
		'poll': poll, 
	}

	print(request.user == poll.user)
	if request.user == poll.user:
		return render(request, 'polls/poll_result.html', context)

	if poll.close:
		return render(request, 'polls/poll_result.html', context)

	if request.user.is_anonymous:
		# if users already voted this poll
		if request.COOKIES.get('poll_%s'%pk) is not None:
			return render(request, 'polls/poll_result.html', context)
	else:
		try:
			entry = get_object_or_404(VoteEntry, question=pk, user=request.user)
			context = {
				'poll': poll,
				'entry': entry
			}
			return render(request, 'polls/poll_result.html', context)
		except:
			pass	

	return render(request, 'polls/poll_detail.html', context)


def create_poll(request):
	option_formset = modelformset_factory(PollOption, fields=('option',), extra=2)

	if request.method == 'POST':
		question_form = PollQuestionForm(request.POST)
		option_form = option_formset(request.POST)

		if question_form.is_valid() and option_form.is_valid():
			question = question_form.save(commit=False)

			if request.user.is_authenticated:
				question.user = request.user

			question.save()
			options = option_form.save(commit=False)

			for option in options:		
				option.question = question
				option.save()

			return redirect(reverse('poll_detail',
				kwargs={'pk': question.id,
			 			'question': question.get_question_slug()}))
	
	question_form = PollQuestionForm()
	option_form = option_formset(queryset=PollOption.objects.none())

	context = {
		'question_form': question_form,
		'option_form': option_form,
	}

	return render(request, 'polls/poll_create.html', context)

@login_required
def profile(request):
	user = request.user
	form = UserForm(instance=user)
	polls = PollQuestion.objects.filter(user=user).order_by("-date")
	context = {
		'polls': polls,
		'form': form,
	}
	
	return render(request, 'polls/profile.html', context)

@login_required
def edit_profile(request):
	user = request.user
	if request.method == 'POST':
		form = UserForm(request.POST, instance=user)
		if form.is_valid():
			form.save()
			return redirect(reverse('profile'))

	else:
		form = UserForm(instance=user)
		context = {'form': form}
		return render(request, 'polls/edit_profile.html', context)



# API Views

class PollDetailAPI(APIView):

	def get(self, request, question, format=None):
		options = PollOption.objects.filter(question=question)
		serializer = PollOptionSerializer(options, many=True)
		response = Response(serializer.data)
		return response

	def put(self, request, question, format=None):
		questionObj = get_object_or_404(PollQuestion, id=question)

		requestData = request.data
		option = get_object_or_404(PollOption, id=requestData['id'], 
			question=requestData['question'], option=requestData['option'])

		serializer = PollOptionSerializer(option)
		data = serializer.data

		# mark poll voted by this browser
		if request.user.is_anonymous:
			# request.session.set_expiry(60*60*24*360)
			option.vote += 1
			option.save()
			data={'is_anonymous': True}
			data.update(serializer.data)
		else:
			# set up vote entry	
			try:
				entry, created = VoteEntry.objects.get_or_create(question=questionObj, 
					user=request.user, voted_option=option)
				if created:
					# update the vote to database if user haven't voted yet
					option.vote += 1
					option.save()
					serializer = PollOptionSerializer(option)
					data = serializer.data
			except Exception as e:
				print(e)

		return Response(data)


class PollQuestionAPI(APIView):

	def put(self, request, question, format=None):
		
		question = get_object_or_404(PollQuestion, id=question)
		serializer = PollQuestionSerializer(question, data=request.data)
		
		if serializer.is_valid():
			if request.user == question.user:
				serializer.save()
				data = serializer.data
				return Response(data)
			else:
				return Response({'error': 'You must be the owner of this poll to edit it.'})
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, question, format=None):
		question = get_object_or_404(PollQuestion, id=question)
		if request.user == question.user:
			question.delete()
		else:
			return Response({'error': 'You must be the owner of this poll to edit it.'})
		return Response(status=status.HTTP_204_NO_CONTENT)

