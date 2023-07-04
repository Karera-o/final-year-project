from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Member
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    # email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

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

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class SigninForm(AuthenticationForm):
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
        #     if self.user_cache is None:
        #         raise forms.ValidationError("Invalid email or password.")
        #     elif not self.user_cache.is_active:
        #         raise forms.ValidationError("This account is inactive.")
        # self.check_for_test_cookie()
        return self.cleaned_data


class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
