# Generated by Django 4.2.2 on 2023-06-24 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0002_remove_staff_mobile_remove_staff_password_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Staff',
        ),
    ]