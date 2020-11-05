
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import Http404
from django.forms import modelformset_factory
from django.core.paginator import Paginator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import PollQuestion, PollOption, VoteEntry
from .forms import PollQuestionForm
from .serializers import PollOptionSerializer, PollQuestionSerializer

from users.forms import UserForm


# Create your views here.

def poll(request):
    all_polls = PollQuestion.objects.all().order_by("-date")
    paginator = Paginator(all_polls, 6)
    page_number = request.GET.get('page')
    all_polls = paginator.get_page(page_number)

    return render(request, 'polls/poll.html', {'all_polls': all_polls})


def poll_detail(request, pk, question):
    poll = get_object_or_404(PollQuestion, pk=pk)
    context = {
        'poll': poll,
    }

    if request.user == poll.user:
        return render(request, 'polls/poll_result.html', context)

    if poll.close:
        return render(request, 'polls/poll_result.html', context)

    # if user already cast their vote
    try:
        entry = VoteEntry.objects.get(question=pk, user=request.user)
        context = {
            'poll': poll,
            'entry': entry
        }
        return render(request, 'polls/poll_result.html', context)
    except VoteEntry.DoesNotExist:
        entry = None

    # if not yet vote
    return render(request, 'polls/poll_detail.html', context)


def create_poll(request):
    option_formset = modelformset_factory(
        PollOption, fields=('option',), extra=2)

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

            return redirect(reverse('poll_detail',
                                    kwargs={'pk': question.id,
                                            'question': question.slug}))

    question_form = PollQuestionForm()
    option_form = option_formset(queryset=PollOption.objects.none())

    context = {
        'question_form': question_form,
        'option_form': option_form,
    }

    return render(request, 'polls/poll_create.html', context)


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

    form = UserForm(instance=user)
    context = {'form': form}
    return render(request, 'polls/edit_profile.html', context)


# API Views

class PollDetailAPI(APIView):

    def get(self, request, question, format=None):
        options = PollOption.objects.filter(question=question)
        if options.exists():
            serializer = PollOptionSerializer(options, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, question, format=None):
        questionObj = get_object_or_404(PollQuestion, id=question)
        option = get_object_or_404(PollOption, id=int(request.data['id']))
        serializer = PollOptionSerializer(option)

        # set up vote entry
        if request.user != questionObj.user:
            try:
                entry, created = VoteEntry.objects.get_or_create(question=questionObj,
                                                                 user=request.user, voted_option=option)
                if created:
                    # update the vote to database if user haven't voted yet
                    option.vote += 1
                    option.save()
                    serializer = PollOptionSerializer(option)
                    return Response({'success': 'your vote has been casted'})
                else:
                    return Response({'error': 'you can only vote once'})
            except Exception as e:
                print(e)

        return Response({'error': 'you can not vote your own poll'})


class PollQuestionAPI(APIView):

    def put(self, request, question, format=None):

        question = get_object_or_404(PollQuestion, id=question)
        serializer = PollQuestionSerializer(question, data=request.data)

        if serializer.is_valid():
            if request.user == question.user:
                serializer.save()
                data = serializer.data
                return Response({'success': 'Your poll is now closed'})
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
