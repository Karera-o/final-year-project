from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Member,Event,Activity,Announcement
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    # email = forms.EmailField(required=True)
    # first_name = forms.CharField(required=True)
    # last_name = forms.CharField(required=True)
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    class Meta:
        model = Member
        fields = ('first_name','last_name','email', 'phone', 'password1', 'password2')

        widgets={
            'first_name':forms.TextInput(attrs={'placeholder':'First name','class':'input'}), 
            'last_name':forms.TextInput(attrs={'placeholder':'Last name','class':'input'}), 
            'email':forms.EmailInput(attrs={'placeholder':'johndoe@gmail.com','class':'input'}), 
            'phone':forms.TextInput(attrs={'placeholder':'0788888888','class':'input'}), 
            'password1':forms.PasswordInput(attrs={'placeholder':'Password','class':'input'}), 
            'password2':forms.PasswordInput(attrs={'placeholder':'comfirm password','class':'input'})
        }



class EventForm(ModelForm):
    
    class Meta:
        model=Event
        fields =('title','budget','department','status','description','due_date','end_date'
        )
    status = forms.ChoiceField(choices=Event.STATUS_CHOICE) 
    
class ActivityForm(ModelForm):
    
    class Meta:
        model=Activity
        fields =('title','event','status','description','due_date','end_date'
        )
    status = forms.ChoiceField(choices=Activity.STATUS_CHOICE) 
    
class AnnouncementForm(ModelForm):
    
    class Meta:
        model=Announcement
        fields =('title','description','due_date'
        )
   

    

