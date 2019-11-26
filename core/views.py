from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from core import models as core_model
from core import serializers as serializer


# Create your views here.

class RegistratonView(APIView):
	serializer_class = serializer.UserSerializer
	permission_classes = (AllowAny,)
	def post(self,request):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		response = serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

