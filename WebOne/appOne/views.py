from django.shortcuts import render,redirect
# from .forms import UserForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# def signup_view(request):
#     if request.method == 'POST'
#     form = UserCreationForm(request.POST)
#     if form.is_valid():
#         form.save()
#         # log the user in
#         return render(request,"appOne/")

def index(request):
    return render(request, 'appOne/index.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        print("A")
        if form.is_valid():
            #log in the user
            return render(request,"appOne/main_page.html")
    else:
        form = AuthenticationForm()
        print("B")
    return render(request,"appOne/login.html",{'form':form})

# Create your views here.
