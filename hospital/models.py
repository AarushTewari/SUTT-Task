from django.db import models
from django.utils import timezone
# Create your models here.

class Staff(models.Model):
    roles = [
        ('oncologist', 'oncologist'),
        ('ent', 'ent'),
        ('cardiologist', 'cardiologist'),
        ('neurologist', 'neurologist'),
        ('orthologist', 'orthologist')
    ]
    name = models.CharField(max_length=50)
    role = models.CharField(choices=roles, max_length=20)    

    def __str__(self):
       return self.name

class Patient(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    email = models.EmailField(null=True, unique=True)
    age = models.IntegerField(null=True)
    address = models.CharField(max_length=50)

    def __str__(self):
       return self.name

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
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

    def __str__(self):
       return self.patient.name
    
class Bill(models.Model):
    amount = models.IntegerField()