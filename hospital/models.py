from django.db import models
from django.utils import timezone
from datetime import datetime
# Create your models here.

class Patient(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    email = models.EmailField(null=True, unique=True)
    age = models.IntegerField(null=True)
    address = models.CharField(max_length=50)

    def __str__(self):
       return self.name
    
class Staff(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(null=True, unique=True)

    def __str__(self):
       return self.username

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    billing_status = [
        ('pending', 'Pending'),
        ('completed', 'Completed')
    ]
    roles = [
        ('oncologist', 'oncologist'),
        ('ent', 'ent'),
        ('cardiologist', 'cardiologist'),
        ('neurologist', 'neurologist'),
        ('orthologist', 'orthologist')
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date1 = models.DateField(default=timezone.now)
    time1 = models.TimeField(default=timezone.now)
    complain = models.TextField(default='No')
    doctor = models.CharField(choices=roles, max_length=30)
    status = models.CharField(choices=STATUS_CHOICES, max_length=30, default='pending')
    cost = models.PositiveIntegerField(default=0)
    billing_status = models.CharField(choices=billing_status, max_length=30, default='pending')

    def __str__(self):
       return self.patient.name
    
class Room(models.Model):
    name = models.CharField(max_length=1000, null=True)
    patient = models.CharField(max_length=200, null=True)
    def __str__(self):
       return self.patient

class message(models.Model):
    value = models.CharField(max_length=100000000)
    date = models.DateTimeField(default= datetime.now, blank=True)
    user = models.CharField(max_length=100000000)
    room = models.CharField(max_length=100000000, blank=True)
