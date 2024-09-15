from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q
from django.utils.http import *
from django.utils.encoding import *



class LoginSerializer(serializers.Serializer):
	username = serializers.CharField(
		required=True
	)
	password = serializers.CharField(
		required=True
	)
	@classmethod
	def validate(self, data):
		errors = {}
		username = data.get("username").lower()
		filterquery = Q()
		filterquery.add (
			Q(is_active=True),
			Q.AND
		)
		instance = User.objects.filter(
			filterquery
		).last()
		if not instance:
			errors["username"] = "This username does not exist."
		if errors:
			raise serializers.ValidationError(errors)

		return super(LoginSerializer, self).validate(self, data)		

