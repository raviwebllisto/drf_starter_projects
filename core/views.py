from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from core import models as core_model
from core import serializers as serializer
#Email Send
from django.core.mail import send_mail
from django.conf import settings


#For Registration 
class RegistratonView(APIView):
    serializer_class = serializer.UserSerializer
    permission_classes = (AllowAny,)

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.save()
        code = str(response.verification_code)
        #Email Verification
        subject = 'Django Email Subject'
        message = 'http://localhost:8000/active/?active_code={}'.format(code)
        # message = code
        email_from = settings.EMAIL_HOST_USER
        user = request.data.get('email')
        recipient_list = [user,]
        send_mail( subject, message, email_from, recipient_list )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

class MailSend(APIView): 
    pass       
    # permission_classes = (AllowAny,)
    # def post(self,request):
    #   subject = 'Django Email Subject' #email sending
    #   message = 'Thank you for register'
    #   recipient_list = ['gurjarraviiet2k13@gmail.com',]
    #   email_from = settings.EMAIL_HOST_USER
    #   send_mail( subject, message, email_from, recipient_list )


class MailVerificationView(APIView):
    serializer_class = serializer.VerificationSeialiser
    permission_classes = (AllowAny,)

    def get(self,request):
        serializer = self.serializer_class(data=request.GET)
        serializer.is_valid(raise_exception=True)
        obj = serializer.get(request)
        return Response(obj)



    