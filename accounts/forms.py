from django import forms

from accounts.models import LecturerProfile, StudentProfile, User, UserProfile  
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True)


    class Meta:
        model=User
        fields=['role','first_name','last_name','email','password1','password2',]

class StudentForm(forms.ModelForm):
    graduation_year = forms.DateField(
        label="Year of graduation",
        widget=forms.TextInput(attrs={'type': 'date'}),
        help_text="Choose estimated year of graduation."
    )

    class Meta:
        model=StudentProfile
        fields="__all__"

class LecturerForm(forms.ModelForm):


    class Meta:
        model=LecturerProfile
        fields="__all__"


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
