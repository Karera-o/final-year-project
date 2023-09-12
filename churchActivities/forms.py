from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import *
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
   
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
   

from django.contrib.auth.models import User, Group

class AssignGroupForm(forms.Form):
    user = forms.ModelChoiceField(queryset=Member.objects.all())
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    department = forms.ModelChoiceField(queryset=Department.objects.all(),required=False)
 
class TitheForm(ModelForm):
    
    class Meta:
        model=TitheOffering
        fields =('offering_type','sabbath','returned','quarter','returner')
    offering_type = forms.ChoiceField(choices=TitheOffering.OFFERING_TYPE) 
    sabbath = forms.ChoiceField(choices=TitheOffering.SABBATH_CHOICE)
    quarter = forms.ChoiceField(choices=TitheOffering.QUARTER_CHOICE)

class DonationForm(ModelForm):

    member = forms.ModelChoiceField(queryset=None,required=False,blank=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    donation_type = forms.ChoiceField(choices=Payment.DONATION_CHOICES)
    # amount = forms.DecimalField(max_digits=10, decimal_places=2)

       
    class Meta:
         model=Payment
         fields = ['donation_type', 'department', 'amount_given']


class BudgetForm(ModelForm):

    class Meta:
        model = Budget
        fields = ['department','amount_from_church','amount_from_members','start_date','end_date',]