from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from .forms import UserForm
from .models import User
from .utils import detectUser, send_verification_email, send_forgot_password_email

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
			
			send_verification_email(request, user)

			return redirect('user_account_activation_link_confirmation')
		else:
			messages.error(request, 'Error in fields.')


	context = {
		'form': form,
	}

	return render(request, 'accounts/registerUser.html', context)
	
	


def user_account_activation_link_confirmation(request):
	return render(request, 'accounts/activation_link_confirmation.html')




def activate(request, uidb64, token):
	try:
		uid = urlsafe_base64_decode(uidb64).decode()
		user = User._default_manager.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	
	if user is not None and default_token_generator.check_token(user, token):
		user.is_active = True
		user.save()
		messages.success(request, 'Congratulations, your account has been activated.')
		return redirect('login_user')
	else:
		messages.error(request, 'Either link is invalid or expired!')
		return redirect('login_user')



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
		return redirect('login_user')

	logout(request)
	return redirect('home')


def myAccount(request):
	if not request.user.is_authenticated:
		messages.warning(request, 'You need to login first to view this page.')
		return redirect('login_user')

	user = request.user
	redirectUrl = detectUser(user)
	return redirect(redirectUrl)


@user_passes_test(check_role_customer)
def customerDashboard(request):
	if not request.user.is_authenticated:
		return redirect('login_user')
	

	return render(request, 'accounts/customerDashboard.html')



def forgot_password(request):
	if request.method == "POST":
		email = request.POST.get('email')

		if User.objects.filter(email__exact=email).exists():
			user = User.objects.get(email=email)

			send_forgot_password_email(request, user)

			messages.success(request, 'Email has been sent your email with a link to reset password')
			return redirect('login_user')
		else:
			messages.error(request, 'Email does not exist. Please enter registerd email address')
			return redirect('forgot_password')

	return render(request, 'accounts/forgot_password.html')



def reset_password_validate(request, uidb64, token):
	try:
		uid = urlsafe_base64_decode(uidb64).decode()
		user = User._default_manager.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and default_token_generator.check_token(user, token):
		request.session['uid'] = uid
		messages.info(request, 'Please reset your password.')
		return redirect('reset_password')
	else:
		messages.error(request, 'Either link is invalid or expired.')
		return redirect('forgot_password')


def reset_password(request):
	if request.method == 'POST':
		password = request.POST.get('password')
		confirm_password = request.POST.get('confirm_password')
		user = User.objects.get(pk=request.session.get('uid'))

		if password == confirm_password:
			user.set_password(password)
			user.is_active = True
			user.save()

			messages.success(request, 'Your password has been updated successfully. You can login now.')
			return redirect('login_user')
		else:
			messages.error(request, 'Passwords do not match!')
			return redirect('reset_password')

	return render(request, 'accounts/reset_password.html')
