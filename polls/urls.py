from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.poll, name='all_poll'),
    path('poll/create/', views.create_poll, name='create_poll'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('poll/<int:pk>/<slug:question>/',
         views.poll_detail, name='poll_detail'),

    path('api/poll/<int:question>/',
         views.PollDetailAPI.as_view(), name='api_poll_detail'),
    path('api/poll-question/<int:question>/',
         views.PollQuestionAPI.as_view(), name='api_poll')
]
