from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from .models import *
from .forms import *
from .filters import *


@unauthenticated_user
def loginPage(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('management')

		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'projects/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def employeePage(request):
	projects = Project.objects.all()
	total_projects = projects.count()

	tasks = Task.objects.all().order_by("-id")
	total_tasks = tasks.count()
	
	mytasks = tasks.filter(assigned_to=request.user) 
	myprojects = projects.filter(program_manager=request.user)
	tasksgiven = tasks.filter(created_by=request.user)

	context = {'projects':projects, 'tasks': tasks, 'mytasks': mytasks, 'myprojects':myprojects, 'tasksgiven': tasksgiven}
	return render(request, 'projects/employee.html', context)

@login_required(login_url='login')
@admin_only
def managementPage(request):
	projects = Project.objects.all()
	total_projects = projects.count()

	tasks = Task.objects.all().order_by("-id")
	total_tasks = tasks.count()

	open_projects = projects.filter(close_project = False)
	open_tasks = tasks.filter(completed=False)
	
	context = {'open_projects': open_projects,'projects':projects, 'open_tasks': open_tasks,'tasks': tasks}

	return render(request, 'projects/management.html', context)

@login_required(login_url='login')
def createProject(request):
	projectForm = ProjectForm()
	fromPage = "create"

	if request.method == 'POST':
		projectForm = ProjectForm(request.POST)
		if projectForm.is_valid():
			projectForm.save()
			messages.info(request, 'Created Project!')
			return redirect('/')
		else:
			messages.warning(request, 'Check From Field for Errors! WO probably already exists.')
	context = {'from': fromPage, 'projectForm': projectForm}

	return render(request,'projects/project_form.html',context)

@login_required(login_url='login')
def updateProject(request, pk):
	project = Project.objects.get(id=pk)
	projectForm = ProjectForm(instance=project)
	fromPage = "update"

	if request.method == 'POST':
		projectForm = ProjectForm(request.POST, instance=project)
		if projectForm.is_valid():
			projectForm.save()
			return redirect('/')


	context = {'from': fromPage,'projectForm': projectForm}
	return render(request,'projects/project_form.html',context)
	
@login_required(login_url='login')
def deleteProject(request, pk):
	project = Project.objects.get(id=pk)
	if request.method == 'POST':
		project.delete()
		return redirect('/')

	context = {'item':project}
	return render(request,'projects/delete.html',context)

@login_required(login_url='login')
def createTask(request, view_complete=False) -> HttpResponse:
	group = request.user.groups.all()[0]
	pm_work_orders = Project.objects.all()
	if group == "employee":
		pm_work_orders = Project.objects.filter(program_manager=request.user)

	form = None

	if request.POST.getlist("add_edit_task"):
		form = TaskForm(
			request.user, 
			request.POST, 
			# initial={"assigned_to": request.user.id},
			)
		if form.is_valid():
			new_task = form.save(commit=False)
			new_task.created_by = request.user
			form.save()
			return redirect('/')
		else:
			messages.warning(request, "Error! Task was not created. Check form for missing fields.")
			print(form.errors)
		
	else:
		form = TaskForm(
			request.user,
			# initial={"assigned_to": request.user.id},
			)

	context = {'form': form, 'group':group,'pm_work_orders':pm_work_orders}
	return render(request,'projects/task_form.html',context)

@login_required(login_url='login')
def updateTask(request, pk):
	task = Task.objects.get(id=pk)
	form = TaskForm(instance=task)

	if request.method == 'POST':
		form = TaskForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			return redirect('/')


	context = {'taskForm': form}
	return render(request,'projects/task_form.html',context)

@login_required(login_url='login')
def updateEmployeeTask(request, pk):
	task = Task.objects.get(id=pk)
	form = EmployeeTaskForm(instance=task)

	if request.method == 'POST':
		form = EmployeeTaskForm(request.POST, instance=task)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'taskForm': form}
	return render(request,'projects/task_form.html',context)

@login_required(login_url='login')
def deleteTask(request, pk):
	task = Task.objects.get(id=pk)
	if request.method == 'POST':
		task.delete()
		return redirect('/')

	context = {'item':task}
	return render(request,'projects/delete.html',context)


@login_required(login_url='login')
def reportPage(request):
	projects = Project.objects.all()
	total_projects = projects.count()

	tasks = Task.objects.all()
	total_tasks = tasks.count()

	context = {'projects':projects, 'tasks': tasks}
	return render(request, 'projects/report.html', context)

@login_required(login_url='login')
def allProjectsPage(request):
	projects = Project.objects.all()
	total_projects = projects.count()

	tasks = Task.objects.all()
	total_tasks = tasks.count()


	myFilter = ProjectFilter(request.GET, queryset=projects)
	projects = myFilter.qs

	context = {'projects':projects, 'tasks': tasks, 'myFilter': myFilter}
	return render(request, 'projects/all_projects.html', context)

@login_required(login_url='login')
def allTasksPage(request):
	projects = Project.objects.all()
	total_projects = projects.count()

	tasks = Task.objects.all()
	total_tasks = tasks.count()

	myFilter = TaskFilter(request.GET, queryset=tasks)
	tasks = myFilter.qs

	context = {'projects':projects, 'tasks': tasks, 'myFilter':myFilter}
	return render(request, 'projects/all_tasks.html', context)

@login_required(login_url='login')
def dailyLog(request):
	form = DailyLogForm()

	if request.method == 'POST':
		form = DailyLogForm(request.POST)
		if form.is_valid():
			form.save()
			messages.info(request, 'Hours Submitted!')
			return redirect('/')
		else:
			messages.warning(request, 'Check From for Errors!')

	projects = Project.objects.all()
	total_projects = projects.count()

	tasks = Task.objects.all()
	total_tasks = tasks.count()

	mytasks = tasks.filter(assigned_to=request.user)
	
	context = {'form': form,'projects':projects, 'total_projects': total_projects, 'tasks': tasks, 'total_tasks': total_tasks, 'mytasks':mytasks}
	return render(request, 'projects/dailylog_form.html', context)