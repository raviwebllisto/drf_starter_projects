import string
import random
# from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from celery import shared_task
# from django.contrib.auth import get_user_model
from core import models as core_model
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def create_random_employee(total):
	for i in range(total):
		first_name = 'emp_{}'.format(get_random_string(10, string.ascii_letters))
		last_name = 'emp_{}'.format(get_random_string(10, string.ascii_letters))
		compny_name = 'emp_{}'.format(get_random_string(10, string.ascii_letters))
		email = '{}@example.com'.format(first_name)
		salary = random.randint(10,99999)
		obj = core_model.Employee(first_name=first_name, last_name=last_name, compny_name=compny_name, email=email, salary=salary)
		obj.save()
	return '{} random users created with success!'.format(total)

@shared_task
def send_mail(total,**kwarg):
	for i in range(total):
		subject = 'Account Verification'
		message = 'Frist Celery message send '
		email_from = settings.EMAIL_HOST_USER
		user = 'ravindra.webllisto@gmail.com'
		recipient_list = [user,]
		send_mail( subject, message, email_from, recipient_list )
	return '{} random email message send'.format(total)