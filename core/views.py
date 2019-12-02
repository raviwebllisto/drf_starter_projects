from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from core import utils
import pyotp
import random
from core import models as core_model
from core import serializers as serializer
#Email Send
from django.core.mail import send_mail
from django.conf import settings

from twilio.rest import Client

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
        subject = 'Account Verification'
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

#Account Verifications
class MailVerificationView(APIView):
    serializer_class = serializer.VerificationSeialiser
    permission_classes = (AllowAny,)

    def get(self,request):
        serializer = self.serializer_class(data=request.GET)
        serializer.is_valid(raise_exception=True)
        obj = serializer.get(request)
        return Response(obj)

#OTP Send API
class SendUserOTPAPIView(generics.CreateAPIView):
    serializer_class = serializer.OTPSerializer
    permission_classes = (AllowAny,)
  
  
    def post(self, request, *args, **kwargs):
        account_sid = settings.TWILIO_ACOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        otp = random.randint(100,99999)
        client = Client(account_sid, auth_token)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.data['phone']
        to_send = [user,]
        obj = core_model.OTPVerification.objects.create(phone=user, code=otp)
        message = client.messages\
        .create(
            body='Hello Ravindra OTP is {}'.format(otp),
            from_='+18589144399',
            to=to_send)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# OTP Verifications
class OTPVerificationView(APIView):
    serializer_class = serializer.OTPVerifySeialiser
    permission_classes = (AllowAny,)

    def get(self,request):
        serializer = self.serializer_class(data=request.GET)
        serializer.is_valid(raise_exception=True)
        obj = serializer.get(request)

        return Response(obj)


class SendRequestView(APIView):
    serializer_class = serializer.SendRequestSerializer
    permission_classes = (AllowAny,)
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.send(request)

        if response["status"]:
            response_status = status.HTTP_200_OK
        else:
            response_status = status.HTTP_404_NOT_FOUND
        return Response(response,status=response_status)

class AcceptRequestView(APIView):
    serializer_class = serializer.AcceptRequestSerializer
    permission_classes =(AllowAny,)

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.accept(request)

        if response["status"]:
            response_status = status.HTTP_201_ok
        else:
            response_status = status.HTTP_404_NOT_FOUND
        return Response(response,status=response_status)