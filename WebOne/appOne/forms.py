from django import forms
from .models import UserProfileInfo, Module
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username','email','password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ('portfolio_site','profile_pic')

class AddModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = '__all__'
        labels = {'module_name': 'Name of module'}


class AddChapterForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = '__all__'
        labels = {'chapter_name': 'Name of chapter'}
