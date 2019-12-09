import string

# from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from celery import shared_task
# from django.contrib.auth import get_user_model
from core import models as core_model

@shared_task
def create_random_user_accounts(total):
	for i in range(total):
		username = 'user_{}'.format(get_random_string(10, string.ascii_letters))
		email = '{}@example.com'.format(username)
		password = get_random_string(50)
		obj = core_model.User(username=username, email=email, password=password)
		obj.save()
	return '{} random users created with success!'.format(total)

# @shared_task
# def emailsend(total):
# 	email=core_model.User.objects.get