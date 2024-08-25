from django.http import HttpResponse
from django.shortcuts import redirect, render

from accounts.models import UserProfile
from .forms import RegistrationForm

# Create your views here.
# def account(request):
#     return HttpResponse("<h1>Hello World! You will create your acct here soon!<h1>")
def landing(request):
    if request.method =='GET' :
        user_type=request.GET.get('type')

    return render(request, 'accounts/landing.html')

def register(request):
    form =RegistrationForm()
    if request.method =='POST':
        form= RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            
            # Create the UserProfile with the selected role
            
            UserProfile.objects.create(user=user, role=role)

            return redirect('/')
        else:
            context ={
            "form":form
            }
            return render(request,'accounts/register.html',context)
    else:

        context ={
            "form":form
        }
        return render(request,'accounts/register.html',context)
    # return render(request,template_name=,context=)