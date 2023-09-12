from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.name

class DepartmentHOD(models.Model):
    department = models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,unique=True)
    hod = models.ForeignKey('Member', on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:

        # return self.hod.first_name + ' ' + self.hod.last_name
        return self.department.name
    
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
        return self.first_name + ' ' + self.last_name


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
    


class TitheOffering(models.Model):
    
    OFFERING_TYPE = (
        ('Tithe', 'Tithe'),
        ('Offerings', 'Offerings'),
        ('Umusaruro', 'Umusaruro'),
        ('Inyubako', 'Inyubako'),
        ('Iteraniro Rikuru', 'Iteraniro Rikuru'),
    )
    SABBATH_CHOICE = (
        ('First Sabbath', 'First Sabbath'),
        ('Second Sabbath', 'Second Sabbath'),
        ('Third Sabbath', 'Third Sabbath'),
        ('Forth Sabbath', 'Forth Sabbath'),
        ('Fifth Sabbath', 'Fifth Sabbath'),
    )

    QUARTER_CHOICE = (
        ('First Quarter', 'First Quarter'),
        ('Second Quarter', 'Second Quarter'),
        ('Third Quarter', 'Third Quarter'),
        ('Forth Quarter', 'Forth Quarter'),
    )

    offering_type = models.CharField(max_length=50, choices=OFFERING_TYPE)
    sabbath = models.CharField(max_length=50, choices=SABBATH_CHOICE)
    quarter = models.CharField(max_length=60, choices=QUARTER_CHOICE)
    returned = models.FloatField()
    date = models.DateField(auto_now=True)
    returner = models.IntegerField()

class Payment(models.Model):
    DONATION_CHOICES = (
        ('Tithe', 'Tithe'),
    ('Offerings', 'Offerings'),
    ('Umusaruro', 'Umusaruro'),
    ('Inyubako', 'Inyubako'),
    ('Iteraniro Rikuru', 'Iteraniro Rikuru'),
    ('Donation', 'Donation'),
    )
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    donation_type = models.CharField(max_length=100, choices=DONATION_CHOICES)
    amount_given = models.FloatField()
    date_created = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.member.first_name + " " + self.member.last_name
    

class Budget(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    amount_from_church = models.FloatField()
    amount_from_members = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    date_created = models.DateField(auto_now=True)
    
    
    def __str__(self):
        return self.department.name