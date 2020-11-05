from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import MyUser
from .forms import CustomUserCreationForm
from .serializers import UserSerializer


# Create your views here.
def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse(settings.LOGIN_URL))
    else:
        form = CustomUserCreationForm()

    context = {'form': form}

    return render(request, 'users/registration.html', context)


class UserAPI(APIView):

    def get(request, format=None):
        users = MyUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
