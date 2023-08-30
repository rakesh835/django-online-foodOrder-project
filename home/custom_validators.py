import os
from django.core.exceptions import ValidationError

def custom_image_validator(value):
	extension = os.path.splitext(value.name)[1]
	print(extension)
	valid_extensions = ['.png', '.jpg', 'jpeg', '.bmp']
	if not extension.lower() in valid_extensions:
		raise ValidationError('Unsupported file extemsion. Allowed extendion are:' + str(valid_extensions))
