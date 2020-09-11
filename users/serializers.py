from rest_framework import serializers

from .models import MyUser

class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = MyUser
		read_only_fields = ['id', 'email']
		fields = ['id', 'email', 'first_name', 'last_name']