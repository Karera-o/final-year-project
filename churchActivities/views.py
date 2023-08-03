from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from .decorators import *
from django.contrib.auth.decorators import login_required

#Signup
def signUp(request):
    pageTitle = 'SignUp'

    if request.method == 'POST':
      
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
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

            if user.groups.filter(name='admin').exists():
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
# @login_required
def userDashboard(request):
    
    user = request.user

    print(user)

    context={
        'user':user,
    }
    if request.headers.get('HX-Request'):
        return render(request, 'pages/index-template.html',context)
    
    return render(request, 'pages/index.html',context)

#Admin dashboard
@is_admin
def adminDashboard(request):

    user = request.user

    # print(user.first_name)
    # print(user.firstname)
    print(user)

    context={
        'user':user,
    }
    if request.headers.get('HX-Request'):
        return render(request, 'pages/index-template.html',context)
    
    return render(request, 'pages/index.html',context)

#User dashboard
def hodDashboard(request):
    
    user = request.user

    print(user)

    context={
        'user':user,
    }
    if request.headers.get('HX-Request'):
        return render(request, 'pages/index-template.html',context)
    
    return render(request, 'pages/index.html',context)
#Members page

def members(request):

    members = Member.objects.all()

    context = {
        
       'members':members,
    }
    
    return render(request, 'pages/members.html',context)

#Events Page
@login_required
def events(request):
    
    events = Event.objects.all()
    
    context={
        'events':events
    }
    
    return render(request, 'pages/events.html',context)

#Activities Page
@login_required
def activities(request):
    
    activities = Activity.objects.all()
    
    context={
        'activities':activities
    }
    
    return render(request, 'pages/activities.html',context)

#Announcements Page
@login_required
def announcements(request):
    
    announcements = Announcement.objects.all()
    
    context={
        'announcements':announcements
    }
    
    return render(request, 'pages/announcements.html',context)

#Logs Page
def logs(request):
    
    return render(request, 'pages/logs.html')
@is_hod
def addEvent(request):
    
    departments = Department.objects.all()
    form = EventForm()
    print('In event 1')
    print('In event 2')
    if request.headers.get('HX-Request'):
        print('hx')
    if request.method == 'POST':
        print('Data are received')
        form = EventForm(request.POST)
        
        if form.is_valid():
            print('Data are valid')
            form.save()
            return redirect('events')
        else:
            print(form.errors)
            print('Errors')
        
    else:
        form = EventForm()
        print('Data are not received')
    context={
        'form':form,
        'departments':departments
    }
        
    return render(request, 'pages/add-event.html',context)
    # return render(request, 'pages/signUp.html',context)
@is_hod
def addActivity(request):
    
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

@is_hod
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
        
@is_hod   
def deletingEvent(request,id):
    
    try:
        event = Event.objects.get(id=id)
    
        event.delete()
    except Exception:
        print('Error')
        
    return redirect('events')
@is_hod
def updateEvent(request,id):
    
    try:
        event = Event.objects.get(id=id)
        if request.method == 'POST':
            form = EventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            
            form = EventForm(instance=event)
            context ={
                'form':form
            }
            return render(request, 'pages/update-event.html',context)
    except Exception:
        print('Error')
        
@is_hod
def deletingActivity(request,id):
    
    try:
        activity = Activity.objects.get(id=id)
    
        activity.delete()
    except Exception:
        print('Error')
        
    return redirect('dashboard')
@is_hod
def updateActivity(request,id):
    
    try:
        activity = Activity.objects.get(id=id)
        if request.method == 'POST':
            form = ActivityForm(request.POST, instance=activity)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
        else:
            
            form = Activity(instance=activity)
            context ={
                'form':form
            }
            return render(request, 'pages/update-activity.html',context)
    except Exception:
        print('Error')
        return redirect('dashboard')
@is_hod        
def deletingAnnouncement(request,id):
    
    try:
        announcement = Announcement.objects.get(id=id)
    
        announcement.delete()
    except Exception:
        print('Error')
        
    return redirect('dashboard')

@is_hod
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

@is_admin
def assignGroup(request):

    
    if request.method == 'POST':
        form = AssignGroupForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            group = form.cleaned_data['group']
            user.groups.add(group)
            return redirect('dashboard') 

        else:
            print(form.errors) 
    else:
        
        form = AssignGroupForm()
    context={
        'form':form,
        
    }
    return render(request, 'pages/assign-group.html',context)
 
from django.http import HttpResponse
from django.views.generic import View
 
#importing get_template from loader
from django.template.loader import get_template
 
#import render_to_pdf from util.py 
from .utils import render_to_pdf 
 
#Creating our view, it is a class based view
class html_to_pdf_view(View):
     def get(self, request, *args, **kwargs):
        
        #getting the template
        pdf = render_to_pdf('pages/index.html')
         
         #rendering the template
        return HttpResponse(pdf, content_type='application/pdf')