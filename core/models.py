from __future__ import unicode_literals
import uuid
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django_common.db_fields import JSONField
from django.contrib.auth.base_user import BaseUserManager



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    # date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=False)
    is_staff = models.BooleanField(default=False)
    # avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    verification_code = models.UUIDField(default=uuid.uuid4, editable=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class OTPVerification(models.Model):
    """
    OTP - One time password
    """
    phone = PhoneNumberField(unique=True)
    code = models.CharField(max_length=8)


# class TimeStampModel(models.Model):
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         abstract = True


class PersonalChat(models.Model):
    chat_id = models.CharField(max_length=100, unique=True)
    conversation = JSONField(null=True, blank=True)


class Friend(models.Model):
    STATUS = (("REQUESTED","requested"),
              ("REJECTED","rejected"),
              ('ACCEPTED','accepted'),
              ('UNFRIEND','unfriend')
            )

    from_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="requset_from_user")

    to_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="request_to_user")
    chat = models.ForeignKey(
        PersonalChat,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="persnal_chat")
    status = models.CharField(max_length=50,choices=STATUS,default='requested')


class MsgModel(models.Model):
    message = models.CharField(max_length=100,null=True,blank=True)


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    compny_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    salary = models.FloatField()
