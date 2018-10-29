from django.shortcuts import render
from user_app.forms import UserForm,UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required #a decorator for some pages where the user needs to be logged in.


def index(request):
    return render(request,'user_app/index.html')

@login_required
def special(request):
    return HttpResponse("Great! You are logged in!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index')) #we wanna make sure only a user who is logged in can logged out. In order to make sure of that we can decorate it with the login_required decorator

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileInfoForm(request.POST)

        if user_form.is_valid and profile_form.is_valid:
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm(request.POST)
        profile_form = UserProfileInfoForm(request.POST)
    return render(request,'user_app/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})

def user_login(request):

    if request.method == 'POST': #if true, means that the user has filled the login info, so we need to get the username and password supplied.
         username = request.POST.get('username') #we're using the POST.get method b'coz we have named the usename label in the login.html file
         password = request.POST.get('password')

         #now we'll use python's built-in authentication function
         user = authenticate(username=username,password=password)

         if user:
             if user.is_active:
                 login(request,user)
                 return HttpResponseRedirect(reverse('index'))
             else:
                 return HttpResponse("Account Not Active")

         else:
            print("Someone tried to login and failed")
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request,'user_app/login.html',{})
