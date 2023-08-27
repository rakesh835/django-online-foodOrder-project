from django.db import models

from accounts.models import User, UserProfile
from accounts.utils import send_approval_email

# Create your models here.

class Vendor(models.Model):
	user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
	user_profile = models.OneToOneField(UserProfile, related_name='UserProfile', on_delete=models.CASCADE)
	vendor_name = models.CharField(max_length=50)
	vendor_license = models.ImageField(upload_to='vendor/license')
	is_approved = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	modeified_at = models.DateTimeField(auto_now=True)


	def __str__(self):
		return self.vendor_name
		

	def save(self, *args, **kwargs):
		if self.pk is not None:
			original_saved = Vendor.objects.get(pk=self.pk)
			
			if self.is_approved != original_saved.is_approved:
				mail_template = 'accounts/emails/admin_approval_email.html'
				context = {
						'user': self.user,
						'is_approved': self.is_approved,
					}
					
				if self.is_approved == True:
					mail_subject = 'Congratulations, Your restaurant has been approved.'
					send_approval_email(mail_subject, mail_template, context)
				else:
					mail_subject = 'Sorry, Your restaurant is not eligible to publish food menu on our marketplace.'
					send_approval_email(mail_subject, mail_template, context)

		return super(Vendor, self).save(*args, **kwargs)