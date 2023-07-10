from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *


#Signup
def signUp(request):
    pageTitle = 'SignUp'

    if request.method == 'POST':
      
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
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
            return redirect('dashboard')
        else:
            print('The user does not exit')
            return render(request, 'pages/signIn.html', {'error': 'Invalid email or password.'})
        
    else:
        
        pass
    return render(request, 'pages/signIn.html')

#Signout 
def signout(request):
    logout(request)
    return redirect('signin')  

#User dashboard
def userDashboard(request):
    
    return render(request, 'pages/index.html')

#Admin dashboard
def adminDashboard(request):

    if request.headers.get('HX-Request'):
        return render(request, 'pages/index-template.html')
    
    return render(request, 'pages/index.html')

#Members page
def members(request):
    
    return render(request, 'pages/members.html')

#Events Page
def events(request):
    
    events = Event.objects.all()
    
    context={
        'events':events
    }
    
    return render(request, 'pages/events.html',context)

#Activities Page
def activities(request):
    
    activities = Activity.objects.all()
    
    context={
        'activities':activities
    }
    
    return render(request, 'pages/activities.html',context)

#Announcements Page
def announcements(request):
    
    announcements = Announcement.objects.all()
    
    context={
        'announcements':announcements
    }
    
    return render(request, 'pages/announcements.html',context)

#Logs Page
def logs(request):
    
    return render(request, 'pages/logs.html')

def addEvent(request):
    
    departments = Department.objects.all()
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('events')
        else:
            print(form.errors)
        
    else:
        form = EventForm()
        
    context={
        'form':form,
        'departments':departments
    }
        
    return render(request, 'pages/add-event.html',context)

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
        
    
def deletingEvent(request,id):
    
    try:
        event = Event.objects.get(id=id)
    
        event.delete()
    except Exception:
        print('Error')
        
    return redirect('dashboard')

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
        

def deletingActivity(request,id):
    
    try:
        activity = Activity.objects.get(id=id)
    
        activity.delete()
    except Exception:
        print('Error')
        
    return redirect('dashboard')

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
        
def deletingAnnouncement(request,id):
    
    try:
        announcement = Announcement.objects.get(id=id)
    
        announcement.delete()
    except Exception:
        print('Error')
        
    return redirect('dashboard')


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

