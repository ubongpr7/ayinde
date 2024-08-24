from django.http import HttpResponse
from django.shortcuts import render
from .forms import RegistrationForm

# Create your views here.
# def account(request):
#     return HttpResponse("<h1>Hello World! You will create your acct here soon!<h1>")

def account(request):
    form =RegistrationForm()
    context ={
        "form":form
    }
    return render(request,'accounts/register.html',context)
    # return render(request,template_name=,context=)