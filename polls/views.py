from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import PollQuestion, PollOption, Tag, Comment, VoteEntry
from .forms import PollForm, PollQuestionForm, UserForm, CommentForm
from django.forms import formset_factory, modelformset_factory, inlineformset_factory

from .serializers import PollOptionSerializer

from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

def poll(request):
	all_polls = PollQuestion.objects.all().order_by("-date")
	return render(request, 'polls/poll.html', {'all_polls': all_polls})

def poll_detail(request, pk):
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
		if request.COOKIES.get('voted') is not None:
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

	
	# if request.method == 'POST': 
	# 	form = PollForm(request.POST)
	# 	if form.is_valid():
	# 		for option in poll.polloption_set.all():
	# 			if form.cleaned_data['option'] == str(option.pk):
	# 				option.vote += 1
	# 				option.save()
	# 				return redirect('poll_result', pk=poll.pk)

	
	return render(request, 'polls/poll_detail.html', context)


def poll_result(request, pk):
	poll = PollQuestion.objects.get(pk=pk)
	comments = Comment.objects.filter(question=poll).order_by('-date')
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.question = poll
			comment.user = request.user
			comment.save()
			return redirect(reverse('poll_result', kwargs={'pk': poll.id}))
	form = CommentForm()
	context = {
		'poll': poll,
		'form': form,
		'comments': comments, 
	}
	return render(request, 'polls/poll_result.html', context)


def create_poll(request):
	if not request.user.is_authenticated:
		return redirect(reverse("login"))
	else:
		option_formset = modelformset_factory(PollOption, fields=('option',), extra=2)

		if request.method == 'POST':
			question_form = PollQuestionForm(request.POST)
			option_form = option_formset(request.POST)
			if question_form.is_valid() and option_form.is_valid():
				question = question_form.save(commit=False)
				question.user = request.user
				question.save()
				options = option_form.save(commit=False)
				for option in options:		
					option.question = question
					option.save()
				return redirect(reverse('poll_result', kwargs={'pk': question.id}))
		
		question_form = PollQuestionForm()
		option_form = option_formset(queryset=PollOption.objects.none())
		context = {
			'question_form': question_form,
			'option_form': option_form,
		}

		return render(request, 'polls/poll_create.html', context)

def delete_poll(request, pk):
	question = get_object_or_404(PollQuestion , pk=pk)
	if question.user == request.user:
		
		question.delete()
		return redirect('profile')
	else:
		return redirect('all_polls')

def profile(request):
	user = request.user
	form = UserForm(instance=user)
	polls = PollQuestion.objects.filter(user=user).order_by("-date")
	context = {
		'polls': polls,
		'form': form,
	}
	
	return render(request, 'polls/profile.html', context)

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

def delete_comment(request, pk):
	comment = Comment.objects.get(id=pk)
	poll = comment.question
	if request.user == comment.user:
		comment.delete()

	return redirect(reverse('poll_result', kwargs={'pk': poll.id}))

def edit_comment(request, pk):
	comment = Comment.objects.get(id=pk)
	poll = comment.question
	if request.user == comment.user:
		if request.method == 'POST':
			form = CommentForm(request.POST, instance=comment)
			if form.is_valid():
				form.save()
				return redirect(reverse('poll_result', kwargs={'pk': poll.id}))

		else:
			form = CommentForm(instance=comment)
			context = {
				'form': form
			}

			return render(request, 'polls/edit_comment.html', context)

	return redirect(reverse('poll_result', kwargs={'pk': poll.id}))


# API Views

class PollDetailAPI(APIView):

	def get(self, request, question, format=None):
		print(request.user.id)
		options = PollOption.objects.filter(question=question)
		serializer = PollOptionSerializer(options, many=True)
		response = Response(serializer.data)
		return response

	def put(self, request, question, format=None):
		optionId = request.data.get('id')
		
		option = get_object_or_404(PollOption, id=optionId)
		question = get_object_or_404(PollQuestion, id=question)
		serializer = PollOptionSerializer(option, data=request.data)

		# set up vote entry
		if serializer.is_valid():
			serializer.save()
			
			data = serializer.data
			# mark poll voted by this browser
			if request.user.is_anonymous:
				data={'is_anonymous': True}
				data.update(serializer.data)
			else:
				try:
					entry = VoteEntry.objects.get_or_create(question=question, voted_option=option, user=request.user)
					entry.save()
					print(entry)
				except:
					pass
			return Response(data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# def update_poll(request, pk):
# 	question = PollQuestion.objects.get(id=pk)
# 	option_formset = inlineformset_factory(PollQuestion, PollOption, fields=('option',), extra=3)

# 	if request.method == 'POST':
# 		question_form = PollQuestionForm(request.POST, instance=question)
# 		option_form = option_formset(request.POST, instance=question)
# 		if question_form.is_valid() and option_form.is_valid():
# 			question_form.save()
# 			option_form.save()
# 			return redirect(reverse('all_poll'))

# 	question_form = PollQuestionForm(instance=question)
# 	option_form = option_formset(instance=question)
# 	context = {
# 		'question_form': question_form,
# 		'option_form': option_form,
# 	}

# 	return render(request, 'polls/poll_update.html', context)

