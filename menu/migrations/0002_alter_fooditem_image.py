# Generated by Django 4.2.4 on 2023-08-31 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='image',
            field=models.ImageField(upload_to='food_images'),
        ),
    ]
