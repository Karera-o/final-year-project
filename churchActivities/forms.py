from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Member

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = Member
        fields = ('first_name','last_name','email', 'phone', 'password', 'password2',   )
        widgets={
            'first_name':forms.TextInput(attrs={'placeholder':'First name','class':'input'}), 
            'last_name':forms.TextInput(attrs={'placeholder':'Last name','class':'input'}), 
            # 'email':forms.EmailInput(attrs={'placeholder':'johndoe@gmail.com','class':'input'}), 
            'phone':forms.TextInput(attrs={'placeholder':'0788888888','class':'input'}), 
            'password1':forms.PasswordInput(attrs={'placeholder':'Password','class':'input'}), 
            'password2':forms.PasswordInput(attrs={'placeholder':'comfirm password','class':'input'})
        }

class SigninForm(forms.Form):
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)
