from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import RegistrationForm

# Create your views here.
# def account(request):
#     return HttpResponse("<h1>Hello World! You will create your acct here soon!<h1>")
def landing(request):
    
    return render(request, 'accounts/landing.html')

def register(request):
    form =RegistrationForm()
    if request.method =='POST':
        form= RegistrationForm(request.POST)
        if form.is_valid():
            

            form.save()
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