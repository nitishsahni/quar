from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'email', 'industry', 'typeOfBusiness', 'website', 'phone', 'companyLogo')

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ('name', 'email', 'dob', 'year', 'phone', 'institution')

class PostForm(forms.ModelForm):
    class Meta:
        model = PostZ
        fields = ('title', 'duration', 'qualification', 'startDate', 'stipend', 'location', 'description', 'requirements')


class ApplyForm(forms.ModelForm):
    class Meta:
        model = Apply
        fields = ('resume', 'cover', 'skills', 'presence')

class ApplyFormCompany(forms.ModelForm):
    class Meta:
        model = Apply
        fields = ('status',)
