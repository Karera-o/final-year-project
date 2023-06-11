from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100)
    hod = models.ForeignKey('Member', on_delete=models.SET_NULL, null=True)

class Member(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=100)

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=100)

class Activity(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    time = models.TimeField()
    status = models.CharField(max_length=100)

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_created = models.DateField()

class Participation(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

class ChurchBoard(models.Model):
    ROLE_CHOICES = (
        ('churchboard', 'Church Board'),
        ('hod', 'HOD'),
    )

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


