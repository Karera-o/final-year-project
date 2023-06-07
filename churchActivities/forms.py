from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Member

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = Member
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone')

class SigninForm(forms.Form):
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)
