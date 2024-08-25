from django import forms

from accounts.models import User  
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    # password=


    class Meta:
        model=User
        fields=['first_name','last_name','email','password1','password2']