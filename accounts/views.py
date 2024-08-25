from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login,authenticate
from django.contrib import messages
from accounts.models import LecturerProfile, UserProfile
from .forms import LecturerForm, LoginForm, RegistrationForm, StudentForm

# Create your views here.
# def account(request):
#     return HttpResponse("<h1>Hello World! You will create your acct here soon!<h1>")
from django.shortcuts import render, redirect, get_object_or_404
from .models import User

def create_profile(request, id, role):
    # Get the user by id
    user = get_object_or_404(User, id=id)
    if request.user.id !=id:
        if role == 'lecturer':
            title='Create Lecture Profile'
            form = LecturerForm()
        else:
            form = StudentForm()
            title='Create Student Profile'


        if request.method == 'POST':
            if role == 'lecturer':
                form = LecturerForm(request.POST)
            else:
                form = StudentForm(request.POST)

            if form.is_valid():
                profile = form.save(commit=False)  # Do not save to the database yet
                profile.user = user  # Assign the user to the profile
                profile.save()  # Save the profile to the database
                return redirect('/')

        context = {
            'form': form,
            'role': role,
            'title':title
        }
        return render(request, 'create.html', context)

    messages.error(request,'Forbidden')
    return redirect('/')



def user_login(request):
    title='Sign in'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in.')
                return redirect('home')  # Redirect to the home page or any other page
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'create.html', {'form': form,'title':title})

def register(request):
    form =RegistrationForm()
    if request.method =='POST':
        form= RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            username = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            # Create the UserProfile with the selected role
            login(request, user)  # Log in the user after registration
            user = authenticate(request, username=username, password=password)

            messages.success(request, "Registration successful.")
            UserProfile.objects.create(user=user, role=role)
            if role=='student':
                
                return redirect(f'/accounts/create-profile/{user.id}/student')
            if role=='lecturer':
                return redirect(f'/accounts/create-profile/{user.id}/lecturer')

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