from django.urls import path
from . import views

urlpatterns = [
	path('', views.poll, name='all_poll'),
	path('(?P<pk>[0-9]+)/(?P<question>[-a-zA-Z0-9_?&*$#@!]+)/$', views.poll_detail, name='poll_detail'),
	path('poll/create/', views.create_poll, name='create_poll'),
	path('profile/', views.profile, name='profile'),
	path('profile/edit/', views.edit_profile, name='edit_profile'),

	path('api/poll/<int:question>/', views.PollDetailAPI.as_view(), name='api_poll_detail'),
	path('api/poll-question/<int:question>/', views.PollQuestionAPI.as_view(), name='api_poll')
]
