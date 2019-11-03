from django import forms
from .models import *
from django.contrib.auth.models import User
#import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

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
        model = Chapter
        exclude = ['module', 'can_start', 'end_datetime']
        labels = {'chapter_name': 'Name of chapter',
                    'chapter_desc': 'Description'}

class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        # fields = '__all__'
        exclude = ['chapter', 'question_number']
        labels = {'question_name' : 'Question statement',
                    'question_optionA': 'Option A',
                    'question_optionB': 'Option B',
                    'question_optionC': 'Option C',
                    'question_optionD': 'Option D' }

class AddSolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        # fields = '__all__'
        exclude = ['question']
        labels = {'solution_answer': 'Correct Answer',
                    'solution_explanation': 'Explanation'}

class PublishChapterForm(forms.Form):
    end_datetime = forms.DateTimeField(label="Date to end chapter")

    def clean_end_datetime(self):
        data = self.cleaned_data['end_datetime']
        
        # Raise error if the end date is in the past. 
        if data < now():
            raise ValidationError(_('Invalid date - end date in the past'))

        # Return the cleaned data.
        return data