from django.shortcuts import render, reverse, redirect
from .forms import CustomUserCreationForm
from django.contrib import messages


# Create your views here.
def registration(request):
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Account created successfully')
			return redirect(reverse('login'))
	
	form = CustomUserCreationForm()
	context = {'form': form}
	
	return render(request, 'users/registration.html', context)