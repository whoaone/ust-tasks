from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('management')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func


def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator


def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name
		if group == 'employee':
			return redirect('employee')
		if group == 'management':
			return view_func(request, *args, **kwargs)
	return wrapper_function


def prevent_recursion(func):
	@wraps(func)
	def no_recursion(sender, instance=None, **kwargs):

		if not instance:
			return

		if hasattr(instance, '_dirty'):
			return

		func(sender, instance=instance, **kwargs)

		try:
			instance._dirty = True
			instance.save()
		finally:
			del instance._dirty

	return no_recursion