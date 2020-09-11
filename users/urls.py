from django.urls import path, include
from . import views

urlpatterns = [
	path('registration/', views.registration, name='registration'),
	path('api/user/', views.UserAPI.as_view(), name='user-api'),
]