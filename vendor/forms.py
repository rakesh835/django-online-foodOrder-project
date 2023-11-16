from django import forms

from .models import Vendor, OpeningHour
from home.custom_validators import custom_image_validator


class VendorForm(forms.ModelForm):
	vendor_license = forms.FileField(widget=forms.FileInput(), validators=[custom_image_validator])

	class Meta:
		model = Vendor
		fields = ['vendor_name', 'vendor_license']




class OpeningHoursForm(forms.ModelForm):
	class Meta:
		model = OpeningHour
		fields = ['day', 'from_hour', 'to_hour', 'is_closed']