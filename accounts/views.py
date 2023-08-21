from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserForm
from .models import User

# Create your views here.


def registerUser(request):
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
			return redirect('home')
		else:
			messages.error(request, 'Error in fields.')


	context = {
		'form': form,
	}

	return render(request, 'accounts/registerUser.html', context)
	
	