from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.

class CustomUserManager(BaseUserManager):

	def create_user(self, email, first_name, last_name, username, password=None):
		if not email:
			raise ValueError('User must have an email.')

		if not username:
			raise ValueError('User must have a username.')

		user = self.model(
				email = self.normalize_email(email),
				first_name = first_name,
				last_name = last_name,
				username = username,
			)

		user.set_password(password)
		user.save(using=self._db)

		return user


	def create_superuser(self, email, first_name, last_name, username, password=None):
		user = self.create_user(
				email = self.normalize_email(email),
				first_name = first_name,
				last_name = last_name,
				username = username,
				password = password
			)

		user.is_superuser = True
		user.is_admin = True
		user.is_active = True
		user.is_staff = True

		user.save(using=self._db)

		return user



class User(AbstractBaseUser):
	RESTAURANT = 1
	CUSTOMER = 2

	ROLE_CHOICE = (
			(RESTAURANT, 'Restaurant'),
			(CUSTOMER, 'Customer'),
		)

	email = models.EmailField(max_length=100, unique=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	username = models.CharField(max_length=30, unique=True)
	phone_number = models.CharField(max_length=13, blank=True)
	role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)
	
	is_superuser = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)

	date_joined = models.DateTimeField(auto_now_add=True)
	last_login = models.DateTimeField(auto_now_add=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

	objects = CustomUserManager()

	def __str__(self):
		return self.email


	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True




class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
	profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
	cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
	address_line_1 = models.CharField(max_length=50, blank=True, null=True)
	address_line_2 = models.CharField(max_length=50, blank=True, null=True)
	country = models.CharField(max_length=15, blank=True, null=True)
	state = models.CharField(max_length=15, blank=True, null=True)
	city = models.CharField(max_length=15, blank=True, null=True)
	pin_code = models.CharField(max_length=5, blank=True, null=True)
	latitude = models.CharField(max_length=20, blank=True, null=True)
	longitude = models.CharField(max_length=20, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)



	def __str__(self):
		return self.user.email




			