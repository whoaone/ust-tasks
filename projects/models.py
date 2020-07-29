import datetime

from django.conf import settings
from django.db import DEFAULT_DB_ALIAS, models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F
from django.urls import reverse
from django.utils import timezone
from django.utils.timezone import now


# from django_currentuser.middleware import (get_current_user, get_current_authenticated_user)
# from django_currentuser.db.models import CurrentUserField

# Create your models here.

def get_name(self):
    return self.first_name + " " + self.last_name

User.add_to_class("__str__", get_name)

# def get(self, queryset=None):
# 	'''This loads the profile of the currently logged in user'''
# 	return User.objects.get(user=self.request.user)

# User.add_to_class("get", get)


class Project(models.Model):
	work_order = models.IntegerField(blank=False, null=True, unique=True)
	proposal_no = models.IntegerField(blank=True, null=True)
	hours_budgeted = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=True)
	hours_used = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
	hours_remaining = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	program_manager = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
	close_project = models.BooleanField(default=False, null=True, blank=False)
	date_created = models.DateTimeField(default=now, editable=False, null=True)
	due_date = models.DateField(blank=True, null=True)

	def __str__(self):
		return str(self.work_order)

class Task(models.Model):
	CATEGORY = (
			("01", "01-SSR"),
			("02", "02-Test Plan"),
			("03", "03-Weight & Balance"),
			("04", "04-Electrical Load Analysis"),
			("05", "05-Process Specification"),
			("06", "06-Certification Plan"),
			("07", "07-Sevice Bulletin"),
			("08", "08-Standards"),
			("09", "09-Engineering, Functional Hazard, Flamm"),
			("10", "10-Manuals (IPC, CMM, AFMS..)"),
			("11", "11-Kit Lists"),
			("12", "12-Airworthiness"),
			("13", "13-EO"),
			("14", "14-Miscellaneious (Performance)"),
			("15", "15-Compliance Reports"),
			("16", "16-Regulatory Airworthiness Assessment (RAA)"),
			("17", "17-Drawing"),
			("18", "18-SolidWorks Model"),
			("19", "19-Research"),
			("20", "20-Training"),
			("21", "21-Other")
		)
	task_no = models.CharField(max_length=100, null=True, blank=True)
	project = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL)
	category = models.CharField(max_length=100, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True, blank = False)
	assigned_to = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		blank=True,
		null=True,
		related_name="todo_assigned_to",
		on_delete=models.CASCADE,
	)
	# assigned_to = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	hours_given = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=True)
	day_used_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
	hours_remaining = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	due_date = models.DateField(blank=True, null=True)

	completed = models.BooleanField(default=False)

	date_created = models.DateTimeField(default=now, editable=False, blank=True,null=True)
	created_by = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		null=True,
		blank=True,
		related_name="todo_created_by",
		on_delete=models.CASCADE,
	)
	completed_date = models.DateField(blank=True, null=True)
	
	def __str__(self):
		return str(self.id)

	def overdue_status(self):
		"Returns whether the Tasks's due date has passed or not."
		if self.due_date and datetime.date.today() > self.due_date:
			return True

	def save(self, **kwargs):
		if self.pk is None:
			self.hours_remaining=self.hours_given
		if self.completed:
			self.completed_date = datetime.datetime.now()
		self.task_no = str(self.project) + "-" + str(self.category) + "-" + str(self.id)
		super(Task, self).save()



# def update_task(sender, instance, created, using, **kwargs):
# 	woCount = sender.objects.filter(project=instance.project).count()
# 	categoryCount = sender.objects.filter(category=instance.category).count()
# 	task_no = str(instance.project) + "-" + str(instance.category) + "-" + str(categoryCount+1)

# 	if created == True:
# 		instance.task_no = task_no
# 		instance.save()
# 	# else:
# 	# 	objs = Task.objects.filter(id=instance.id)
# 	# 	for obj in objs:
# 	# 		obj.save()

		

# post_save.connect(update_task, sender=Task)

class DailyLog(models.Model):
	CATEGORY = (
			("01", "01-SSR"),
			("02", "02-Test Plan"),
			("03", "03-Weight & Balance"),
			("04", "04-Electrical Load Analysis"),
			("05", "05-Process Specification"),
			("06", "06-Certification Plan"),
			("07", "07-Sevice Bulletin"),
			("08", "08-Standards"),
			("09", "09-Engineering, Functional Hazard, Flamm"),
			("10", "10-Manuals (IPC, CMM, AFMS..)"),
			("11", "11-Kit Lists"),
			("12", "12-Airworthiness"),
			("13", "13-EO"),
			("14", "14-Miscellaneious (Performance)"),
			("15", "15-Compliance Reports"),
			("16", "16-Regulatory Airworthiness Assessment (RAA)"),
			("17", "17-Drawing"),
			("18", "18-SolidWorks Model"),
			("19", "19-Research"),
			("20", "20-Training"),
			("21", "21-Other")
		)
	task_no = models.ForeignKey(Task, null=True, on_delete=models.SET_NULL)
	project = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL)
	category = models.CharField(max_length=100, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True, blank = True)

	hours_given = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
	hours_used = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
	date_created = models.DateTimeField(default=now, editable=False, blank=True,null=True)
	created_by = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		null=True,
		blank=True,
		related_name="log_created_by",
		on_delete=models.CASCADE,
	)

class DailyLogItem(models.Model):
	task = models.ForeignKey(Task, null=True, on_delete=models.SET_NULL)
	time_spent = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)


# 	def __str__(self):
# 		return str(self.id)

# 	def save(self, **kwargs):
# 		# if self.pk is None:
# 		# 	self.hours_remaining=self.hours_given
# 		# if self.completed:
# 		# 	self.completed_date = datetime.datetime.now()
# 		super(DailyLog, self).save()
