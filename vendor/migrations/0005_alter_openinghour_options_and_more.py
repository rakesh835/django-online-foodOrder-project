# Generated by Django 4.2.4 on 2023-11-02 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0004_openinghour'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='openinghour',
            options={'ordering': ('day', '-from_hour')},
        ),
        migrations.AlterUniqueTogether(
            name='openinghour',
            unique_together={('vendor', 'day', 'from_hour', 'to_hour')},
        ),
    ]
