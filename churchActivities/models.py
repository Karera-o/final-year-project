from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=100)
    hod = models.ForeignKey('Member', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.name

class Member(AbstractUser):
    MEMBER_STATUS = [
        ('Regular Member','Regular Member'),
        ('Visitor','Visitor'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(primary_key=True, unique=True)
    phone = models.CharField(max_length=10)
    status = models.CharField(max_length=255, choices=MEMBER_STATUS)
    password = models.CharField(max_length=100)
    username = models.EmailField(unique=True)

    

    def __str__(self):
        return self.username


class Event(models.Model):
    
    STATUS_CHOICE = [
        ('Pending','Pending'),
        ('Completed','Completed'),
        ('Canceled','Canceled'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    due_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=100,choices=STATUS_CHOICE)
    
    def __str__(self):
        return self.title

class Activity(models.Model):
    STATUS_CHOICE = [
        ('Pending','Pending'),
        ('Completed','Completed'),
        ('Canceled','Canceled'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    due_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    date_created = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.title

class Participation(models.Model):
    Member = models.ForeignKey(Member, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.Member.first_name + ' '+ self.Member.last_name

class ChurchBoard(models.Model):
    ROLE_CHOICES = (
        ('churchboard', 'Church Board'),
        ('hod', 'HOD'),
    )

    Member = models.ForeignKey(Member, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    def __str__(self):
        return self.Member.first_name + ' '+ self.Member.last_name


