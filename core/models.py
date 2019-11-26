from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, User
)
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class User(AbstractBaseUser):
	phone = PhoneNumberField(null=True,blank=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=50)
	email = models.EmailField(unique=True)
	username = models.CharField(max_length=100, unique=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

