from django import forms

from accounts.models import User  


class RegistrationForm(forms.ModelForm):
    # password=
    password = forms.CharField(widget=forms.PasswordInput,required=True)


    class Meta:
        model=User
        fields=['first_name','last_name','email','password']