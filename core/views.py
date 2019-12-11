from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from core import utils
import pyotp
import random
import time
from core import models as core_model
from core import serializers as serializer
#Email Send
from django.core.mail import send_mail
from django.conf import settings
#send otp using twilio
from twilio.rest import Client

#chatapp
from django.utils.safestring import mark_safe
import json
#decorators use
from django.contrib.auth.decorators import login_required
from decorators import timeit

import logging
import sys, os


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
    permission_classes = (AllowAny,)
    @timeit
    def get(*args, **kwargs):
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
        try:
          account_sid = settings.TWILIO_ACOUNT_SID
          auth_token = settings.TWILIO_AUTH_TOKEN
          otp = random.randint(10,99999)
          client = Client(account_sid, auth_token)
          serializer = self.serializer_class(data=request.data)
          serializer.is_valid(raise_exception=True)
          phone = serializer.data['phone']
          to_send = [phone,]
          obj = core_model.OTPVerification.objects.create(phone=phone, code=otp)
          message = client.messages\
          .create(
              body='Hello Ravindra OTP is {}'.format(otp),
              from_='+18589144399',
              to=to_send)
          return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as err:

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msg = {
                 "error": err,
                 "line_no": exc_tb.tb_lineno,
                 "file_name": fname,
            }
            logging.error(msg)
            logging.warning(msg)
            loggig.info(msg)
        return Response({'message': 'data'})


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
    permission_classes = (IsAuthenticated,)
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
    permission_classes =(IsAuthenticated,)

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.accept(request)

        if response["status"]:
            response_status = status.HTTP_201_ok
        else:
            response_status = status.HTTP_404_NOT_FOUND
        return Response(response,status=response_status)

#chatapp
def index(request):
    return render(request, 'index.html', {})


def room(request, room_name):
    return render(request, 'room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

class EmployeeView(APIView):
    serializer_class = serializer.EmployeeSerializer
    permission_classes = (AllowAny,)

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        emp = core_model.Employee.objects.all()
        serializer = self.serializer_class(emp,many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        emp = core_model.Employee.objects.get(pk=pk)
        serializer = self.serializer_class(emp,data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    
    def delete(self,request,pk):
        emp = core_model.Employee.objects.get(pk=pk)
        emp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EmployeeList(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = core_model.Employee.objects.all()
    serializer_class = serializer.EmployeeSerializer

class EmployeeDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (AllowAny,)
    queryset = core_model.Employee.objects.all()
    serializer_class = serializer.EmployeeSerializer