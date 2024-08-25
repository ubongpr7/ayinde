from django import forms

from accounts.models import User, UserProfile  
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    # password=
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True)


    class Meta:
        model=User
        fields=['role','first_name','last_name','email','password1','password2',]