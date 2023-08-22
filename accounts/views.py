from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from .forms import UserForm
from .models import User
from .utils import detectUser

# Create your views here.

# restrict user from accessing vendor page
def check_role_customer(user):
	if user.role == 2:
		return True
	else:
		raise PermissionDenied


def registerUser(request):
	if request.user.is_authenticated:
		messages.warning(request, 'Your are already registerd.')
		return redirect('myAccount')

	form = UserForm(request.POST or None)

	if request.method == 'POST':
		
		if form.is_valid():
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			email = form.cleaned_data.get('email')
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			confirm_password = form.cleaned_data.get('confirm_password')

			
			user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username)
			user.set_password(password)

			user.role = User.CUSTOMER
			user.save()
			messages.success(request, 'Registered successfully.')
			return redirect('myAccount')
		else:
			messages.error(request, 'Error in fields.')


	context = {
		'form': form,
	}

	return render(request, 'accounts/registerUser.html', context)
	
	


def login_user(request):
	if request.user.is_authenticated:
		messages.warning(request, 'Your are already logged in.')
		return redirect('myAccount')

	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')

		user = authenticate(email=email, password=password)

		if user is not None:
			login(request, user)
			return redirect('myAccount')
		else:
			messages.warning(request, 'Please enter valid credentials.')
			return redirect('login_user')

	return render(request, 'accounts/login_user.html')



def logout_user(request):
	if not request.user.is_authenticated:
		return redirect('login')

	logout(request)
	return redirect('home')


def myAccount(request):
	if not request.user.is_authenticated:
		messages.warning(request, 'You need to login first to view this page.')
		return redirect('login')

	user = request.user
	redirectUrl = detectUser(user)
	return redirect(redirectUrl)


@user_passes_test(check_role_customer)
def customerDashboard(request):
	if not request.user.is_authenticated:
		return redirect('login')
	

	return render(request, 'accounts/customerDashboard.html')



