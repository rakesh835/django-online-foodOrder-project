from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def detectUser(user):
	if user.role == 1:
		redirectUrl = 'vendorDashboard'
	elif user.role == 2:
		redirectUrl = 'customerDashboard'
	else:
		redirectUrl = '/admin'

	return redirectUrl




def send_verification_email(request, user):
	current_site = get_current_site(request)
	mail_subject = 'Please activate your account'
	message = render_to_string('accounts/emails/send_verification_email.html', {
		'user': user,
		'domain': current_site,
		'uid': urlsafe_base64_encode(force_bytes(user.pk)),
		'token': default_token_generator.make_token(user),
		})

	to_email = user.email
	mail = EmailMessage(mail_subject, message, to=[to_email])
	mail.send()
    


def send_forgot_password_email(request, user):
	current_site = get_current_site(request)
	mail_subject = 'Reset your password'
	message = render_to_string('accounts/emails/send_forgot_password_email.html', {
		'user': user,
		'domain': current_site,
		'uid': urlsafe_base64_encode(force_bytes(user.pk)),
		'token': default_token_generator.make_token(user),
		})

	to_email = user.email
	mail = EmailMessage(mail_subject, message, to=[to_email])
	mail.send()


def send_approval_email(mail_subject, mail_template, context):
	message = render_to_string(mail_template, context)
	to_email = context['user'].email
	mail = EmailMessage(mail_subject, message, to=[to_email])
	mail.send()