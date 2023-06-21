# Generated by Django 4.2.2 on 2023-06-21 13:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='password',
        ),
        migrations.RemoveField(
            model_name='staff',
            name='username',
        ),
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=30),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='date1',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='doctor',
            field=models.CharField(choices=[('oncologist', 'oncologist'), ('ent', 'ent'), ('cardiologist', 'cardiologist'), ('neurologist', 'neurologist'), ('orthologist', 'orthologist')], max_length=30),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time1',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
    ]