from django_cron import CronJobBase, Schedule
from core import models as core_model
from django.core.mail import send_mail
from django.conf import settings


class MyCronJob(CronJobBase):
	RUN_EVERY_MINS = 1 
	# ALLOW_PARALLEL_RUNS = True
	# RETRY_AFTER_FAILURE_MINS = 1

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS,)
	code = 'core.corn.MyCronJob'    # a unique code

	def do(self):

		subject = 'Account Verification'
		message = 'Frist Celery message send '
		email_from = settings.EMAIL_HOST_USER
		user = 'ravindra.webllisto@gmail.com'
		recipient_list = [user,]
		send_mail( subject, message, email_from, recipient_list )
		return '{} random email message send'.format(total)
		# try:
		# 	obj = core_model.EmployeeMode.objects.all()
		# except:
		# 	obj = False

		# if obj:
		# 	obj.delete()
		# 	obj.save
		# content = {'message': 'Hello, World!'}
		# LOGGERS = {'message': 'Hello, World!'}
