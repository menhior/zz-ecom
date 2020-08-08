from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

"""def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return render(request, 'shop/authentication.html')
		return wrapper_func
	return decorator"""

def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name
			

		if group == 'customer':
			return redirect('store')

		if group == 'admin':
			return view_func(request, *args, **kwargs)

	return wrapper_function