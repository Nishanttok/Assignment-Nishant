from django.shortcuts import render
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from account.serializers import *
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.hashers import *
from django.contrib.auth import authenticate, login
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import jwe
from django.conf import settings
import json
import datetime,time
from django.utils.http import *
from django.utils.encoding import *
from rest_framework.parsers import MultiPartParser


class LoginView(GenericAPIView):
	"""
		Enter the username or email and password to login in this project
	"""
	permission_classes = (AllowAny,)
	serializer_class = LoginSerializer
	@classmethod
	@swagger_auto_schema(operation_summary="login api for project",tags=['Account'])
	def post(self, request, *args, **kwargs):
		response = {}
		status_code = 200
		data = request.data
		data_validation = LoginSerializer(data=data)
		is_valid_data = data_validation.is_valid()
		if is_valid_data:
			data = data_validation.validated_data
			username = data.get('username').lower()
			password = data.get('password')
			filterquery = Q()
			filterquery.add (
				Q(is_active=True),
				Q.AND
			)
			instance = User.objects.filter(
				filterquery
			)
			if instance.last():
				instance = instance.last()
				if instance.is_active:
					username = instance.username
					user = authenticate(
						username=username,
						password=password
					)

					if user:
						response["message"] = "success"
						response["name"] = str(instance.first_name) + str(instance.last_name)
						response["email"] = instance.email
					else:
						response["errors"] = {"username":["Username or password is wrong"]}
						status_code = 400
				else:
					response["errors"] = {"username":["Your account is not active"]}
					status_code = 400
			else:
				response["errors"] = {"username":["Username is wrong"]}
				status_code = 400
		else:
			status_code = 400
			response["errors"] = data_validation.errors
		return Response(response, status=status_code)
