from django.urls import path
from . import views

urlpatterns = [
	path('', views.poll, name='all_poll'),
	path('poll/<int:pk>/', views.poll_detail, name='poll_detail'),
	path('poll/<int:pk>/result', views.poll_result, name='poll_result'),
	path('poll/create/', views.create_poll, name='create_poll'),
	path('poll/delete/<int:pk>', views.delete_poll, name='delete_poll'),
	path('profile/', views.profile, name='profile'),
	path('profile/edit', views.edit_profile, name='edit_profile'),
	path('delete_comment/<int:pk>/', views.delete_comment, name='delete_comment'),
	path('edit_comment/<int:pk>/', views.edit_comment, name='edit_comment')
]
