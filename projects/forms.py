from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import Group

from .models import *

# class DateInput(forms.DateInput):
# 	input_type='date'

class ProjectForm(ModelForm):
	due_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), required=False)
	close_project = forms.BooleanField(required=False)
	
	class Meta:
		model = Project
		fields = '__all__'
		# exclude = ['user']
		
class TaskForm(ModelForm):
	def __init__(self, user, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if user.groups.filter(name='employee').exists():
			self.fields['project'].queryset = Project.objects.filter(program_manager=user)

	due_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), required=False)
	completed = forms.BooleanField(required=False)
	
	def clean_created_by(self):
		return self.instance.created_by
		
	class Meta:
		model = Task
		fields = '__all__'
		exclude = []

class EmployeeTaskForm(ModelForm):
	class Meta:
		model = Task
		fields = '__all__'
		exclude = []
	# class Meta:
	# 	model = Task
	# 	fields = ['project', 'category', 'description', 'assigned_to', 'hours_given', 'due_date', 'created_by']
	# 	widgets = {
	# 		'due_date': DateInput(),
	# 	}

class DailyLogForm(ModelForm):
	completed = forms.BooleanField(required=False)
	class Meta:
		model = Task
		fields = '__all__'
		# exclude = ['user']


# class OrderForm(ModelForm):
# 	class Meta:
# 		model = Order
# 		fields = '__all__'

# class CreateUserForm(UserCreationForm):
# 	class Meta:
# 		model = User
# 		fields = ['username', 'email', 'password1', 'password2']
