from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from .forms import VendorForm
from accounts.forms import UserForm
from accounts.models import UserProfile, User

# Create your views here.

# restrict user from accessing vendor page
def check_role_vendor(user):
	if user.role == 1:
		return True
	else:
		raise PermissionDenied



def registerVendor(request):
	form = UserForm(request.POST or None)
	vendor_form = VendorForm(request.POST or None, request.FILES or None)

	
	if request.method == 'POST':
		if vendor_form.is_valid() and form.is_valid():
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			email = form.cleaned_data.get('email')
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username)
			user.set_password(password)
			user.role = User.VENDOR
			user.save()

			vendor = vendor_form.save(commit=False)
			vendor.user = user
			user_profile = UserProfile.objects.get(user=user)
			vendor.user_profile = user_profile
			vendor.save()

			messages.success(request, 'Vendor is registered successfully. Please wait for approval.')
			return redirect('home')


	context = {
	 	'vendor_form': vendor_form,
	 	'form': form,
	 }

	return render(request, 'vendor/registerVendor.html', context)



@user_passes_test(check_role_vendor)
def vendorDashboard(request):
	if not request.user.is_authenticated:
		return redirect('login')

	return render(request, 'vendor/vendorDashboard.html')