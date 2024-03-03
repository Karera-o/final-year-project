from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from .decorators import *
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User, Group
from datetime import datetime
from django.db.models.functions import ExtractYear
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum


from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse


import requests
import json
from paypack.transactions import Transaction

from django.http import JsonResponse
from django.http import HttpResponseServerError


from io import BytesIO
from django.http import HttpResponse, HttpResponseServerError
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

import requests
import math
import random
import os

from django.http import HttpResponse

isNotAdmin = True
isNotHod = True
# global totalActivities
# global totalEvents
# global totalBudget

def eventsData(request):
    user = request.user
    events = []

    # if request.headers.get('HX-Request') and request.method=='POST':
    #     year = int(request.POST['year'])

    # else:
    year = datetime.now().year
    
    # not user.is_superuser or  not user.groups.filter(name='Admin') or not 
    if user.groups.filter(name='HOD') and not user.groups.filter(name='Admin'):
        department = DepartmentHOD.objects.get(hod=user)
        events = Event.objects.annotate(year=ExtractYear('due_date')).filter(department=department.department,year=year)
    else:
        events = Event.objects.all()
    
    completed_events = 0
    pending_events = 0
    canceled_events = 0
    for event in events:
        if event.status == 'Completed':
            completed_events += 1
        if event.status == 'Pending':
            pending_events += 1
        if event.status == 'Canceled':
            canceled_events += 1
    global totalEvents  
    totalEvents = completed_events + pending_events + canceled_events
    isNotHod = True
    if user.groups.filter(name='HOD').exists():
        isNotHod = False
        
    context={
        'events':events,
        'isNotAdmin':isNotAdmin,
        'isNotHod': isNotHod,
        'completed_events':completed_events,
        'pending_events': pending_events,
        'canceled_events':canceled_events,
        'totalEvents':totalEvents,


    }
    
    return context

@login_required
def activities(request):
    
    user = request.user
    activities = []
    if user.groups.filter(name='HOD') and not user.groups.filter(name='Admin'):
        department = DepartmentHOD.objects.get(hod=user)
        events = Event.objects.filter(department=department.department)
        for event in events:

            activities += Activity.objects.filter(event=event)
    else:
        activities = Activity.objects.all()

    completed_activities = 0
    pending_activities = 0
    canceled_activities = 0
    for activity in activities:
        if activity.status == 'Completed':
            completed_activities += 1
        if activity.status == 'Pending':
            pending_activities += 1
        if activity.status == 'Canceled':
            canceled_activities += 1
    global totalActivities
    totalActivities = completed_activities + pending_activities + canceled_activities
    
    isNotHod = True
    if user.groups.filter(name='HOD').exists():
        isNotHod = False
    context={
        'activities':activities,
        'isNotAdmin':isNotAdmin,
        'isNotHod': isNotHod,
        'completed_activities':completed_activities,
        'pending_activities': pending_activities,
        'canceled_activities':canceled_activities,
        'totalActivities':totalActivities,
    }
    
    return render(request, 'pages/activities.html',context)


class BudgetReport(View):
    def get(self, request, *args, **kwargs):
        # Get the template
        template = get_template('Reports/budget-report.html')
        year = datetime.now().year
        user = request.user
        department = None
    # not user.is_superuser or  not user.groups.filter(name='Admin') or not 
        if user.groups.filter(name='HOD') and not user.groups.filter(name='Admin'):
            department = DepartmentHOD.objects.get(hod=user)
            budget = Budget.objects.annotate(year=ExtractYear('start_date')).filter(department=department.department,year=year)
        else:
            
            budget = Budget.objects.all()


        churchTotal = budget.aggregate(churchTotal=Sum('amount_from_church'))['churchTotal']
        membersTotal = budget.aggregate(membersTotal=Sum('amount_from_members'))['membersTotal']

        global totalBudget
        totalBudget = churchTotal + membersTotal
        budgets = {}

        donationTotal = 0
        for item in budget:

            total = Payment.objects.filter(department=item.department).aggregate(total=Sum('amount_given'))['total']
            if total is None:
                total = 0

            donationTotal += total
            budgets[item] = total

        print(donationTotal)
            
        
        if department == None:
            department = ''

        

        from datetime import date
        date_now = date.today
        image = 'static/Images/adventist.jpg'
        context={
        
        'date':date_now,
        'image':image,
        'budgets':budgets,
        'department':department,
        'churchTotal':churchTotal,
        'membersTotal':membersTotal,
        'donationTotal':donationTotal,

        }
        
         # Provide any context data required by your template

        # Render the template
        html = template.render(context)

        # Create a PDF instance
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        
        return HttpResponse("Error generating PDF", status=500)

#Signup
def signUp(request):
    pageTitle = 'SignUp'

    if request.method == 'POST':
      
        form = SignupForm(request.POST)
        if form.is_valid():
            
            
            user = form.save()
            group = Group.objects.get(name='NormalUser')
            user.groups.add(group)
            login(request, user)
            if user.groups.filter(name='admin').exists():
                return redirect('dashboard')
            elif user.groups.filter(name='HOD').exists():
                return redirect('hod-dashboard')
            elif user.groups.filter(name='church_board').exists():
                return redirect('dashboard')
            else:
                return redirect('user-dashboard')
        else:
            print(form.errors)

    else:
        form = SignupForm()
    
    context = {
        'pageTitle': pageTitle,
        'form': form
    }
    
    return render(request, 'pages/signUp.html',context)

#Signin Page
def signIn(request):
    
    if request.method == 'POST':
      
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)

            if user.groups.filter(name='admin').exists() or user.is_superuser:
                return redirect('dashboard')
            elif user.groups.filter(name='HOD').exists():
                return redirect('hod-dashboard')
            elif user.groups.filter(name='church_board').exists():
                return redirect('dashboard')
            else:
                return redirect('user-dashboard')
            
        else:
            print('The user does not exit')
            return render(request, 'pages/signIn.html', {'error': 'Invalid email or password.'})
        
    else:
        
        pass
    return render(request, 'pages/signIn.html')

#Signout 
@login_required
def signout(request):
    logout(request)
    return redirect('signin')  

#User dashboard
@login_required
def userDashboard(request):
    
    user = request.user
    groups = user.groups.all()
    group = ''

    for item in groups:
        print(item)
        group= 'Church Mermber'
    group= 'Church Mermber'
    print(group)
    context = eventsData(request)
    context1={
        'user':user,
        'isNotAdmin':isNotAdmin,
        'isNotHod': isNotHod,
        'group':group,
    }
    context.update(context1)
    if request.headers.get('HX-Request'):

        return render(request, 'pages/events.html',context)
    
    return render(request, 'pages/event-template.html',context)
        

#Admin dashboard
# @is_hod
# @is_admin
def adminDashboard(request):

    user = request.user

    groups = user.groups.all()
    year = datetime.now().year
    activities = []
    if user.groups.filter(name='HOD') and not user.groups.filter(name='Admin'):
        department = DepartmentHOD.objects.get(hod=user)
        events = Event.objects.filter(department=department.department)
        for event in events:

            activities += Activity.objects.filter(event=event)
    else:
        activities = Activity.objects.all()


    completed_activities = 0
    pending_activities = 0
    canceled_activities = 0
    for activity in activities:
        if activity.status == 'Completed':
            completed_activities += 1
        if activity.status == 'Pending':
            pending_activities += 1
        if activity.status == 'Canceled':
            canceled_activities += 1
    global totalActivities
    totalActivities = completed_activities + pending_activities + canceled_activities

    if user.groups.filter(name='HOD') and not user.groups.filter(name='Admin'):
        department = DepartmentHOD.objects.get(hod=user)
        budget = Budget.objects.annotate(year=ExtractYear('start_date')).filter(department=department.department,year=year)
    else:
            
        budget = Budget.objects.all()


    churchTotal = budget.aggregate(churchTotal=Sum('amount_from_church'))['churchTotal']
    membersTotal = budget.aggregate(membersTotal=Sum('amount_from_members'))['membersTotal']

    global totalBudget
    totalBudget = churchTotal + membersTotal

    for item in groups:
        group= item
    print(group)
   
    print(user)
    isAdmin = False
    if user.groups.filter(name='Admin').exists() or user.is_superuser:
        isAdmin = True
    print(user.is_superuser)

    totalEvents= eventsData(request)["totalEvents"]

    context={
        'user':user,
        'isAdmin':isAdmin,
        'group':group,
        'activities':activities,
        'totalEvents': totalEvents,
        'totalActivities': totalActivities,
        'totalBudget': totalBudget,
        'completed_activities': completed_activities,
        
    }
    if request.headers.get('HX-Request'):
        return render(request, 'pages/index-template.html',context)
    
    return render(request, 'pages/index.html',context)

@is_hod
def hodDashboard(request):
    
    user = request.user
    
    groups = user.groups.all()
    totalEvents= eventsData(request)["totalEvents"]
    year = datetime.now().year
    activities = []
    if user.groups.filter(name='HOD') and not user.groups.filter(name='Admin'):
        department = DepartmentHOD.objects.get(hod=user)
        events = Event.objects.filter(department=department.department)
        for event in events:

            activities += Activity.objects.filter(event=event)
    else:
        activities = Activity.objects.all()


    completed_activities = 0
    pending_activities = 0
    canceled_activities = 0
    for activity in activities:
        if activity.status == 'Completed':
            completed_activities += 1
        if activity.status == 'Pending':
            pending_activities += 1
        if activity.status == 'Canceled':
            canceled_activities += 1
    global totalActivities
    totalActivities = completed_activities + pending_activities + canceled_activities

    if user.groups.filter(name='HOD') and not user.groups.filter(name='Admin'):
        department = DepartmentHOD.objects.get(hod=user)
        budget = Budget.objects.annotate(year=ExtractYear('start_date')).filter(department=department.department,year=year)
    else:
            
        budget = Budget.objects.all()


    churchTotal = budget.aggregate(churchTotal=Sum('amount_from_church'))['churchTotal']
    membersTotal = budget.aggregate(membersTotal=Sum('amount_from_members'))['membersTotal']

    global totalBudget
    totalBudget = churchTotal + membersTotal

    for item in groups:
        group= item
    print(group)
    department = DepartmentHOD.objects.get(hod=request.user)

    isNotHod=False
    context={
        'user':user,
        'isNotAdmin':isNotAdmin,
        'isNotHod': isNotHod,
        'department':department,
        'group':group,
        'activities':activities,
        'totalEvents': totalEvents,
        'totalActivities': totalActivities,
        'totalBudget': totalBudget,
        'completed_activities': completed_activities,
        
    }
    if request.headers.get('HX-Request'):
        return render(request, 'pages/index-template.html',context)
    
    return render(request, 'pages/index.html',context)
#Members page

def members(request):

    members = Member.objects.all()

    context = {
        
       'members':members,
       'isNotAdmin':isNotAdmin,
        'isNotHod': isNotHod,
    }
    
    return render(request, 'pages/members.html',context)


#Events Page
@login_required
def events(request):

    context = eventsData(request)

    return  render(request, 'pages/events.html',context)

#Activities Page
@login_required
def activities(request):
    
    user = request.user
    activities = []
    if user.groups.filter(name='HOD') and not user.groups.filter(name='Admin'):
        department = DepartmentHOD.objects.get(hod=user)
        events = Event.objects.filter(department=department.department)
        for event in events:

            activities += Activity.objects.filter(event=event)
    else:
        activities = Activity.objects.all()

    completed_activities = 0
    pending_activities = 0
    canceled_activities = 0
    for activity in activities:
        if activity.status == 'Completed':
            completed_activities += 1
        if activity.status == 'Pending':
            pending_activities += 1
        if activity.status == 'Canceled':
            canceled_activities += 1
    global totalActivities
    totalActivities = completed_activities + pending_activities + canceled_activities
    
    isNotHod = True
    if user.groups.filter(name='HOD').exists():
        isNotHod = False
    context={
        'activities':activities,
        'isNotAdmin':isNotAdmin,
        'isNotHod': isNotHod,
        'completed_activities':completed_activities,
        'pending_activities': pending_activities,
        'canceled_activities':canceled_activities,
        'totalActivities':totalActivities,
    }
    
    return render(request, 'pages/activities.html',context)

#Announcements Page
@login_required
def announcements(request):
    
    announcements = Announcement.objects.all()
    user = request.user
    isNotHod = True
    if user.groups.filter(name='HOD').exists():
        isNotHod = False
    context={
        'announcements':announcements,
        'isNotAdmin':isNotAdmin,
        'isNotHod': isNotHod,
    }
    
    return render(request, 'pages/announcements.html',context)

#Logs Page
def logs(request):
    
    return render(request, 'pages/logs.html')
# @is_hod
def addEvent(request):
    
    departments = Department.objects.all()

    for department in departments:
        print(department.name)
        print(department.id)
    department = DepartmentHOD.objects.get(hod=request.user)
    
    form = EventForm()
    
    if request.headers.get('HX-Request'):
        print('hx')
    if request.method == 'POST':
        print('Data are received')
        form = EventForm(request.POST)
        
        if form.is_valid():
            print('Data are valid')
            # departem = request.POST.get(department)
            # print(departem.department.name)
            form.save()
            return redirect('events')
        else:
            print(form.errors)
            print('Errors')
        
    else:
        form = EventForm()
        print('Data are not received')
    print(department.department.name)
    print(department.id)   
    context={
        'form':form,
        'departments':departments,
        'department':department,
    }
        
    return render(request, 'pages/add-event.html',context)
    
# @is_hod
def addActivity(request):

    user = request.user
    if not user.is_superuser or  not user.groups.filter(name='Admin'):
        department = DepartmentHOD.objects.get(hod=user)
        events = Event.objects.filter(department=department.department)
        # activities = Activity.objects.filter(event=event)
    else:
        # activities = Activity.objects.all()
        events = Event.objects.all()
    
    form = ActivityForm()
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('activities')
        else:
            print(form.errors)
        
    else:
        form = ActivityForm()
        
    context={
        'form':form,
        'events':events
    }
        
    return render(request, 'pages/add-activity.html',context)

# @is_hod
def addAnnouncement(request):
    

    form = AnnouncementForm()
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('announcements')
        else:
            print(form.errors)
        
    else:
        form = AnnouncementForm()
        
    context={
        'form':form,
    }
        
    return render(request, 'pages/add-announcement.html',context)
        
# @is_hod   

# @is_hod
def updateEvent(request,id):
    department = DepartmentHOD.objects.get(hod=request.user)
    try:
        event = Event.objects.get(id=id)
        print(event.title)
        if request.method == 'POST':
            print('received')
            form = EventForm(request.POST, instance=event)
            if form.is_valid():
                print('success')
                form.save()
                return redirect('events')
            
            else:
                print (form.Errors)
        else:
            print('hi')
            form = EventForm(instance=event)
            context ={
                'form':form,
                'department':department,
                'id':id,
            }
            return render(request, 'pages/update-event.html',context)
    except Exception:
        print('Error')
        return redirect('events')
    
def deletingEvent(request,id):
    
    try:
        event = Event.objects.get(id=id)
    
        event.delete()
    except Exception:
        print('Error')
        
    return redirect('events')
# @is_hod
def deletingActivity(request,id):
    
    try:
        activity = Activity.objects.get(id=id)
    
        activity.delete()
    except Exception:
        print('Error')
        
    return redirect('activities')
# @is_hod
def updateActivity(request,id):
    
    try:
        activity = Activity.objects.get(id=id)
        print(activity.title)
        if request.method == 'POST':
            print('received activity')
            form = ActivityForm(request.POST, instance=activity)
            if form.is_valid():
                print('success')
                form.save()
                return redirect('activities')
            else:
                print(form.errors)
        else:
            
            form = ActivityForm(instance=activity)
            context ={
                'form':form,
                'id':id,
            }
            return render(request, 'pages/update-activity.html',context)
    except Exception:
        print('Error')
        return redirect('activities')
# @is_hod        
def deletingAnnouncement(request,id):
    
    try:
        announcement = Announcement.objects.get(id=id)
    
        announcement.delete()
    except Exception:
        print('Error')
        
    return redirect('dashboard')

# @is_hod
def updateAnnouncement(request,id):
    
    try:
        announcement = Announcement.objects.get(id=id)
        if request.method == 'POST':
            form = AnnouncementForm(request.POST, instance=announcement)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            
            form = Announcement(instance=announcement)
            context ={
                'form':form
            }
            return render(request, 'pages/update-announcement.html',context)
    except Exception:
        print('Error')
        return redirect('dashboard')

# @is_admin
def assignGroup(request):

    
    if request.method == 'POST':
        form = AssignGroupForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            group = form.cleaned_data['group']
            
            department = form.cleaned_data['department']
            if user.groups.filter(name='NormalUser').exists():
                user.groups.remove('NormalUser')
            user.groups.add(group)
            
            if department != None:

                depart = DepartmentHOD(
                    department=department,
                    hod=user
                )
                depart.save()

            return redirect('dashboard') 

        else:
            print(form.errors) 
    else:
        
        form = AssignGroupForm()
    context={
        'form':form,
        
    }
    return render(request, 'pages/assign-group.html',context)


@login_required
def titheOfferings(request):
    
    activities = TitheOffering.objects.all().order_by('-date')
    user = request.user
    isNotHod = True
    if user.groups.filter(name='HOD').exists():
        isNotHod = False
    context={
        'activities':activities,
        'isNotAdmin':isNotAdmin,
        'isNotHod': isNotHod,
    }
    
    return render(request, 'pages/tithe-offering.html',context)

def addTitheOfferings(request):
    
    activities = TitheOffering.objects.all().order_by('-date')
    form = TitheForm()
    if request.method == 'POST':
        form = TitheForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('tithe')
        else:
            print(form.errors)
        
    else:
        form = TitheForm()
        
    context={
        'form':form,
        'activities':activities
    }
        
    return render(request, 'pages/add-tithe-offering.html',context)
 




class html_to_pdf_view(View):
    def get(self, request, *args, **kwargs):
        # Get the template
        template = get_template('Reports/report.html')

        activities = TitheOffering.objects.all().order_by('-date')

        quarter1Total = 0
        quarter2Total = 0
        quarter3Total = 0
        quarter4Total = 0

        tithe1 = 0
        tithe2 = 0
        tithe3 = 0
        tithe4 = 0

        for activity in activities:
             
            if activity.quarter == 'First Quarter':
                 quarter1Total += activity.returned

                 if activity.offering_type == 'Tithe':
                     tithe1 += activity.returned 
                 
            elif activity.quarter == 'Second Quarter':
                 quarter2Total += activity.returned

                 if activity.offering_type == 'Tithe':
                     tithe2 += activity.returned 
        
            elif activity.quarter == 'Third Quarter':
                 quarter3Total += activity.returned

                 if activity.offering_type == 'Tithe':
                     tithe3 += activity.returned 
        
            elif activity.quarter == 'Fourth Quarter':
                 quarter4Total += activity.returned

                 if activity.offering_type == 'Tithe':
                     tithe4 += activity.returned 
        
        

        from datetime import date
        date_now = date.today
        image = 'static/Images/adventist.jpg'
        context={
        'activities':activities,
        'date':date_now,
        'image':image,
        'quarter1Total':quarter1Total,
        'quarter2Total':quarter2Total,
        'quarter3Total':quarter3Total,
        'quarter4Total':quarter4Total,
        'tithe1':tithe1,
        'tithe2':tithe2,
        'tithe3':tithe3,
        'tithe4':tithe4,
        }
        print(date)
         # Provide any context data required by your template

        # Render the template
        html = template.render(context)

        # Create a PDF instance
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        
        return HttpResponse("Error generating PDF", status=500)
    

class BudgetReport(View):
    def get(self, request, *args, **kwargs):
        # Get the template
        template = get_template('Reports/budget-report.html')
        year = datetime.now().year
        user = request.user
        department = None
    # not user.is_superuser or  not user.groups.filter(name='Admin') or not 
        if user.groups.filter(name='HOD') and not user.groups.filter(name='Admin'):
            department = DepartmentHOD.objects.get(hod=user)
            budget = Budget.objects.annotate(year=ExtractYear('start_date')).filter(department=department.department,year=year)
        else:
            
            budget = Budget.objects.all()


        churchTotal = budget.aggregate(churchTotal=Sum('amount_from_church'))['churchTotal']
        membersTotal = budget.aggregate(membersTotal=Sum('amount_from_members'))['membersTotal']

        global totalBudget
        totalBudget = churchTotal + membersTotal
        budgets = {}

        donationTotal = 0
        for item in budget:

            total = Payment.objects.filter(department=item.department).aggregate(total=Sum('amount_given'))['total']
            if total is None:
                total = 0

            donationTotal += total
            budgets[item] = total

        print(donationTotal)
            
        
        if department == None:
            department = ''

        

        from datetime import date
        date_now = date.today
        image = 'static/Images/adventist.jpg'
        context={
        
        'date':date_now,
        'image':image,
        'budgets':budgets,
        'department':department,
        'churchTotal':churchTotal,
        'membersTotal':membersTotal,
        'donationTotal':donationTotal,

        }
        
         # Provide any context data required by your template

        # Render the template
        html = template.render(context)

        # Create a PDF instance
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        
        return HttpResponse("Error generating PDF", status=500)
    
class ActivityReport(View):
    def get(self, request, *args, **kwargs):
        # Get the template
        template = get_template('Reports/activity-report.html')
        year = datetime.now().year
        user = request.user
        activities = []
        department = None
        if user.groups.filter(name='HOD') and not user.groups.filter(name='Admin'):
            department = DepartmentHOD.objects.get(hod=user)
            events = Event.objects.filter(department=department.department)
            
            for event in events:

                activities += Activity.objects.filter(event=event)
        else:
            activities = Activity.objects.all()

        if department == None:
            department = ''

        from datetime import date
        date_now = date.today
        image = 'static/Images/adventist.jpg'
        context={
        'activities':activities,
        'date':date_now,
        'image':image,
        'department':department
        }
        print(date)
         # Provide any context data required by your template

        # Render the template
        html = template.render(context)

        # Create a PDF instance
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        
        return HttpResponse("Error generating PDF", status=500)

class EventReport(View):
    def get(self, request, *args, **kwargs):
        # Get the template
        template = get_template('Reports/event-report.html')

        year = datetime.now().year
        user = request.user
        events =[]
        department = None
    # not user.is_superuser or  not user.groups.filter(name='Admin') or not 
        if user.groups.filter(name='HOD') and not user.groups.filter(name='Admin'):
            department = DepartmentHOD.objects.get(hod=user)
            events = Event.objects.annotate(year=ExtractYear('due_date')).filter(department=department.department,year=year)
            
        else:
            events = Event.objects.all()

        totalBudget = events.aggregate(total=Sum('budget'))['total']
        if department == None:
                department = ''
        from datetime import date
        date_now = date.today
        image = 'static/Images/adventist.jpg'
        context={
        'events':events,
        'date':date_now,
        'image':image,
        'department':department,
        'totalBudget':totalBudget,
        }
        
         # Provide any context data required by your template

        # Render the template
        html = template.render(context)

        # Create a PDF instance
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        
        return HttpResponse("Error generating PDF", status=500)
    
class DonationReport(View):
    def get(self, request, *args, **kwargs):
        # Get the template
        template = get_template('Reports/donation-report.html')

        year = datetime.now().year
        user = request.user
        events =[]
        department = None
        isNormalUser = False
    # not user.is_superuser or  not user.groups.filter(name='Admin') or not 
        if user.groups.filter(name='HOD') and not user.groups.filter(name='Admin'):
            department = DepartmentHOD.objects.get(hod=user)
            payments = Payment.objects.annotate(year=ExtractYear('date_created')).filter(department=department.department,year=year)

        elif not user.groups.filter(name='HOD') and not user.groups.filter(name='Admin'):
            payments = Payment.objects.annotate(year=ExtractYear('date_created')).filter(member=user,year=year)
            isNormalUser = True
        else:
            payments = Payment.objects.all()

        totalPayments = payments.aggregate(total=Sum('amount_given'))['total']
        if department == None:
                department = ''
        from datetime import date
        date_now = date.today
        image = 'static/Images/adventist.jpg'
        context={
        'payments':payments,
        'date':date_now,
        'image':image,
        'department':department,
        'totalPayments':totalPayments,
        'isNormalUser':isNormalUser,
        'user':user,
        }
        
         # Provide any context data required by your template

        # Render the template
        html = template.render(context)

        # Create a PDF instance
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        
        return HttpResponse("Error generating PDF", status=500)



def sendEmail(request):
    send_mail(
        subject='Testing Email',
        message='Write an amazing message',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=['kareraol1@gmail.com']
    )
    

    return HttpResponse('The message sent!')


def payment(request):

    user = request.user
    payments= []
    

    year = datetime.now().year
    
    # not user.is_superuser or  not user.groups.filter(name='Admin') or not 
    if user.groups.filter(name='HOD') and not user.groups.filter(name='Admin'):
        department = DepartmentHOD.objects.get(hod=user)
        payments = Payment.objects.annotate(year=ExtractYear('date_created')).filter(department=department.department,year=year)
        departments = 1
        donors = 4

    elif not user.groups.filter(name='HOD') and not user.groups.filter(name='Admin'):
        print ('Found')
        payments = Payment.objects.annotate(year=ExtractYear('date_created')).filter(member=user,year=year)
        donors = 6
        departments = 4
    else:
        payments = Payment.objects.all()
        donors = 6
        departments = 4

    total = payments.aggregate(total=Sum('amount_given'))['total']

    context={
        'payments': payments,
        'departments': departments,
        'donors' :donors,
        'total' :total,

    }

    return render(request, 'pages/payment.html',context)

# from django.views.generic import View
# from django.http import JsonResponse
# from django_flutterwave import Flutterwave

# def payment(request):
#     amount = request.POST['amount']
#     email = request.POST['email']
#     phone_number = request.POST['phone_number']
#     product_description = request.POST['product_description']

#     secret = 'FLWSECK_TEST-db88fbb83c738dd8a56a0664c296a06c-X'
#     flutterwave = Flutterwave(
#         secret_key=secret,
#         env='test'
#     )

#     amount = 100
#     email= 'olivierkarera2020@gmail.com'
#     phone_number='0780732171'
#     product_description='Test'
#     response = flutterwave.charge(
#         amount=amount,
#         email=email,
#         phone_number=phone_number,
#         product_description=product_description
#     )

#     if response.status == 'success':
#         return JsonResponse({'status': 'success'})
#     else:
#         return JsonResponse({'status': 'error', 'message': response.message})


# from python_flutterwave import payment

# class Response:

#     status = 'success'


# def paymente(request):

#     payment.token = 'FLWSECK_TEST-db88fbb83c738dd8a56a0664c296a06c-X'
#     uri = payment.initiate_payment(tx_ref="qwerty", amount=100, redirect_url='payment',
#                                payment_options='mobilemoneyrwanda', customer_email='olivierkarera2020@gmail.com',
#                                customer_phone_number='0780732171', currency='RWF', customer_name='John Doe',
#                                title='Demo Payment', description='Just pay me...')
#     print(uri)
#     details = payment.get_payment_details(transaction_id)
#     print(details)

#     response = Response()
#     response.status = 'success'
#     if response.status == 'success':
#         return JsonResponse({'status': 'success'})
#     else:
#         return JsonResponse({'status': 'error', 'message': response.message})


def paymentFlutter(request,user,amount):
# FLWSECK-936224a16e1619610fbd6df5c2d221ae-18a3253e92dvt-X


#FLWSECK_TEST-83f1f44f7960a45b467de7bb57e1c9d2-X
    user = request.user
   
    # auth_token ='FLWSECK_TEST-192dbf3ff340f7a78724385909279c8d-X'
    # hed ={'Authorization':'Bearer '+auth_token,'Content-Type':'application/json'}
    # data = {
          
    #       "tx_ref": ''+str(math.floor(1000000 + random.random()*9000000)),
    #       "amount": amount,
    #       "currency": "RWF",
    #       "redirect_url": "http://localhost:8000/payment/",
    #       "payment_options": "mobilemoneyrwanda,card",
          
    #       "customer": {
    #         "email": user.email,
    #         "phone_number": user.phone,
    #         'name': user.first_name+' '+user.last_name,
    #       },
    #       "customizations": {
    #         "title": "Auca Church Activities Management System",
    #         "description": "Helping the church to Grow.",
    #         "logo": "static/Images/adventist.jpg",
    #       },
    #     }

    # url= 'https://api.flutterwave.com/v3/payments'
    
    # response = requests.post(url, json=data, headers=hed)
    # response = response.json()
    # print(response)

    # link = response['data']['link']
    # print(link)
    return {"Hello": "response"}
 


def paymentFlutterWave(request):
    from paypack.client import HttpClient

    client_id="8555a5c6-519a-11ee-af6a-deaddb65b9c2"
    client_secret="55cc09cb4c4c0bf05e0dbf6e83cec0deda39a3ee5e6b4b0d3255bfef95601890afd80709"

    HttpClient(client_id=client_id, client_secret=client_secret)

    cashin = Transaction().cashin(amount=100, phone_number="0780732171", mode="development")   
    print(cashin)   
    return render(request, 'pages/donation.html')


def redirectPayment(request,link):

    return redirect(link)

def addBudget(request):
    
    department = DepartmentHOD.objects.get(hod=request.user)
    
    form = BudgetForm()
    

    if request.method == 'POST':
        print('Data are received')
        form = BudgetForm(request.POST)
        
        if form.is_valid():
            print('Data are valid')
            
            form.save()
            return redirect('budget')
        else:
            print(form.errors)
            print('Errors')
        
    else:
        form = BudgetForm()
        print('Data are not received')

    context={
        'form':form,

        'department':department,
    }
        
    return render(request, 'pages/add-budget.html',context)


def budget(request):
    user = request.user
    budget= []

    year = datetime.now().year
    
    # not user.is_superuser or  not user.groups.filter(name='Admin') or not 
    if user.groups.filter(name='HOD') and not user.groups.filter(name='Admin'):
        department = DepartmentHOD.objects.get(hod=user)
        budget = Budget.objects.annotate(year=ExtractYear('start_date')).filter(department=department.department,year=year)

    

    else:
        budget = Budget.objects.all()
    
   
    isNotHod = True
    if user.groups.filter(name='HOD').exists():
        isNotHod = False
        
    context={
        'budget':budget,
        'isNotAdmin':isNotAdmin,
        'isNotHod': isNotHod,
        # 'completed_events':completed_events,
        # 'pending_events': pending_events,
        # 'canceled_events':canceled_events,
        # 'totalEvents':totalEvents,


    }
    
    return render(request, 'pages/budget.html',context)

# from paypack.client import HttpClient
# from paypack.transactions import Transaction



# userPay = None
def paypack(request):

    from paypack.client import HttpClient

    client_id="e6237f9a-d944-11ee-a4b9-deaddb65b9c2"
    client_secret="cbf4e2bb442b3803582632ec572adc9ada39a3ee5e6b4b0d3255bfef95601890afd80709"

    HttpClient(client_id=client_id, client_secret=client_secret)

    user = request.user
    # cashin = Transaction().cashin(amount=100, phone_number="0780732171", mode="development")
    # print("View")
    if request.method=='POST':

        print("Post")

        form = DonationForm(request.POST)
        if form.is_valid():
            print("Valid")

            instance = form.save(commit=False)
            instance.member = user
            global userPay 
            userPay = instance
            # instance.save()
            # 0791920368
            cashin = Transaction().cashin(amount=float(instance.amount_given), phone_number="0791920368", mode="development")
            print(cashin)
            return redirect('payment')
        else:
            print(form.errors)

    form = DonationForm()
    context ={
        'form': form,
        'user': user,
    }
            
    return render(request, 'pages/donation.html',context)

@csrf_exempt
def paypack1(request):

    try:

        body = json.loads(request.body)
    
    except Exception:
        print("Error: ....")
    
    if request.method == 'POST':

        if body["data"]["status"] == 'successful':
            print(body)
            userPay.save()
            image = 'static/Images/adventist.jpg'
            context = {
                "firstname":userPay.member.first_name,
                "amount": userPay.amount,
                "date_created": userPay.date_created,
                "donation_type": userPay.donation_type,
                "image": image

            }
            return render(request, 'Reports/payment-receipt.html', context)

        elif body["data"]["status"] == 'failed':
            print('The transaction failed...')

        else:
            print('Oops.....')

    if request.method == 'GET':
        print(request.method)
        print(body)
    else:
        print("Waiting...")
    # userPay.save()
    image = 'static/Images/adventist.jpg'
    context = {
                "firstname":'Olivier',
                "amount": 100,
                "date_created": "date",
                "donation_type": "test",
                "image": image

            }
    print(context)
    return redirect('events')
    # return render(request, 'Reports/payment-receipt.html', context)

    # print(body)
    # return HttpResponse('Success')