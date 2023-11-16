from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.template.defaultfilters import slugify
from django.db import IntegrityError

from .forms import VendorForm, OpeningHoursForm
from accounts.forms import UserForm, UserProfileForm
from accounts.models import UserProfile, User
from accounts.utils import send_verification_email
from .models import Vendor, OpeningHour
from .utils import get_vendor

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
			vendor_name = vendor_form.cleaned_data.get('vendor_name')
			vendor.vendor_slug = username+'-'+slugify(vendor_name)
			user_profile = UserProfile.objects.get(user=user)
			vendor.user_profile = user_profile
			vendor.save()

			send_verification_email(request, user)

			return redirect('vendor_account_activation_link_confirmation')


	context = {
	 	'vendor_form': vendor_form,
	 	'form': form,
	 }

	return render(request, 'vendor/registerVendor.html', context)



def vendor_account_activation_link_confirmation(request):
	return render(request, 'vendor/vendor_account_activation_link_confirmation.html')



@user_passes_test(check_role_vendor)
def vendorDashboard(request):
	if not request.user.is_authenticated:
		return redirect('login_user')

	return render(request, 'vendor/vendorDashboard.html')



@user_passes_test(check_role_vendor)
def vendor_profile(request):
	if not request.user.is_authenticated:
		return redirect('login_user')
	user_profile = get_object_or_404(UserProfile, user=request.user)
	vend_profile = get_object_or_404(Vendor, user=request.user)

	if request.method == 'POST':
		user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
		vendor_form = VendorForm(request.POST, request.FILES, instance=vend_profile)

		if user_profile_form.is_valid() and vendor_form.is_valid():
			user_profile_form.save()
			vendor_form.save()

			messages.success(request, 'Your vendor profile is updated successfully.')
			return redirect('vendor_profile')
		else:
			messages.error(request, 'Please enter valid field values.')
			return redirect('vendor_profile')


	else:
		user_profile_form = UserProfileForm(instance=user_profile)
		vendor_form = VendorForm(instance=vend_profile)


	context = {
			'user_profile_form': user_profile_form,
			'vendor_form': vendor_form,
			'user_profile': user_profile,
			'vend_profile': vend_profile,
	}

	return render(request, 'vendor/vendor_profile.html', context)




def openingHour(request):
	opening_hours = OpeningHour.objects.filter(vendor=get_vendor(request))

	form = OpeningHoursForm()


	context = {
			'form': form,
			'opening_hours': opening_hours,

	}

	return render(request, 'vendor/openingHour.html', context)



def add_opening_hours(request):
	if request.user.is_authenticated:
		if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
			day = request.POST.get('day')
			from_hour = request.POST.get('from_hour')
			to_hour = request.POST.get('to_hour')
			is_closed = request.POST.get('is_closed')
			
			try:
				hour = OpeningHour.objects.create(vendor=get_vendor(request), day=day, from_hour=from_hour, to_hour=to_hour, is_closed=is_closed)	
				if hour:
					day = OpeningHour.objects.get(id=hour.id)
					if day.is_closed:
						response = {'status': 'success', 'id': hour.id, 'day': day.get_day_display(), 'is_closed': 'Closed'}
				else:
						response = {'status': 'success', 'id': hour.id, 'day': day.get_day_display(), 'from_hour': hour.from_hour, 'to_hour': hour.to_hour}
				return JsonResponse(response)
			except IntegrityError as e:
				response = {'status': 'failed', 'message': 'Provided hours already exist!'}
				return JsonResponse(response)
		else:
			return HttpResponse("Invalid request")


def remove_opening_hours(request, pk=None):
	if request.user.is_authenticated:
		if request.headers.get('x-requested-with') == 'XMLHttpRequest':
			hour = OpeningHour.objects.get(pk=pk)
			hour.delete()
			response = {'status': 'success', 'id': pk}

			return JsonResponse(response)