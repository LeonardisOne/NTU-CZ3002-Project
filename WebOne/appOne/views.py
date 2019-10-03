from django.shortcuts import render, get_object_or_404
from .forms import *

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
# below is deprecated
#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required

#make sure you have form name whenever you are dealing with form.
# Create your views here.
@login_required
def index(request):
    return render(request, 'appOne/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")

"""this is decorator, to highlight that user_logout
   happens only user logged in alr"""
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']


            profile.save()
            registered = True
            return HttpResponseRedirect(reverse('index'))
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'appOne/registration.html',
                    {'user_form':user_form,
                     'profile_form':profile_form,
                     'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index')) #back to home page

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied!")

    else:
        return render(request,'appOne/login.html',{})

@permission_required('appOne.add_module', raise_exception=True)
def add_module(request):
    if request.method == 'POST':
        form = AddModuleForm(request.POST)

        if form.is_valid():
            module = form.save()
            module.save()

            return HttpResponseRedirect(reverse('index'))
    else:
        form = AddModuleForm()

    context = {
        'form': form,
    }
    return render(request, 'appOne/addmodule.html', context)

@permission_required('appOne.add_chapter', raise_exception=True)
def add_chapter(request, pk):
    module_stored = get_object_or_404(Module, module_name=pk)
    if request.method == 'POST':
        form = AddChapterForm(request.POST)
        print('before valid check')

        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.module = module_stored
            chapter.save()
            print('after valid check')

            return HttpResponseRedirect(reverse('index'))
    else:
        form = AddChapterForm()

    context = {
        'form': form,
        'module': module_stored
    }
    return render(request, 'appOne/addchapter.html', context)