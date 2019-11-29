from django_cron import CronJobBase, Schedule
from core import models as core_model

class MyCronJob(CronJobBase):
	RUN_EVERY_MINS = 1 
	# ALLOW_PARALLEL_RUNS = True
	# RETRY_AFTER_FAILURE_MINS = 1

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS,)
	code = 'core.corn.MyCronJob'    # a unique code

	def do(self):
		try:
			obj = core_model.EmployeeMode.objects.all()
		except:
			obj = False

		if obj:
			obj.delete()
			obj.save
		# content = {'message': 'Hello, World!'}
		# LOGGERS = {'message': 'Hello, World!'}
