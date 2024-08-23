from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# def account(request):
#     return HttpResponse("<h1>Hello World! You will create your acct here soon!<h1>")

def account(request):
    return render(request,'accounts/register.html',)
    # return render(request,template_name=,context=)