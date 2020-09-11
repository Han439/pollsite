from django.shortcuts import render, reverse, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import MyUser
from .serializers import UserSerializer


# Create your views here.
def registration(request):
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(reverse('login'))
	else:
		form = CustomUserCreationForm()
		
	context = {'form': form}
	
	return render(request, 'users/registration.html', context)

class UserAPI(APIView):

	def get(request, format=None):
		users = MyUser.objects.all()
		serializer = UserSerializer(users, many=True)
		return Response(serializer.data)

	def put(request, format=None):

		if request.user.is_authenticated:
			user = request.user
			serializer = UserSerializer(user, request.data)
			if serializer.is_valid:
				serializer.save()
				return Response(serializer.data)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)