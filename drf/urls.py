"""drf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views
from rest_framework_simplejwt import views as jwt_views
from django.conf.urls import include


urlpatterns = [
    path('chat/', include('core.urls')),
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/',views.RegistratonView.as_view()),
    path('hello/',views.HelloView.as_view()),
    path('active/',views.MailVerificationView.as_view()),
    path('send-otp/',views.SendUserOTPAPIView.as_view()),
    path('verify-otp/',views.OTPVerificationView.as_view()),
    path('send_request/',views.SendRequestView.as_view()),
    path('accept_request/',views.AcceptRequestView.as_view()),
    path('emp/',views.EmployeeView.as_view()),
    path('emp/<int:pk>/', views.EmployeeView.as_view()),

    path('emplist/',views.EmployeeList.as_view()),
    path('empdetails/',views.EmployeeDetail.as_view()),




]
