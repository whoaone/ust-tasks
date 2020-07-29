import django_filters
from django_filters import DateFilter, CharFilter, BooleanFilter

from .models import *

class ProjectFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name="date_created", lookup_expr='gte')
	end_date = DateFilter(field_name="date_created", lookup_expr='lte')
	class Meta:
		model = Project
		fields = '__all__'
		exclude = ['hours_budgeted', 'hours_used', 'hours_remaining', 'due_date', 'date_created']

class TaskFilter(django_filters.FilterSet):
	start_date = DateFilter(field_name="date_created", lookup_expr='gte')
	end_date = DateFilter(field_name="date_created", lookup_expr='lte')
	# note = CharFilter(field_name='note', lookup_expr='icontains')
	class Meta:
		model = Task
		fields = '__all__'
		#exclude = ['customer', 'date_created']