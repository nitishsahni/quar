from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *

class SignupForm(UserCreationForm):
    industryChoices = \
        [('FA', "Finance and Accounting")
        ,('MA', "Marketing")
        , ('DE', "Design")
        , ('DS', "Data Analytics and Stats")
        , ('PS', "Programming and Software")
        , ('SC', "Supply Chain")
        , ('FS', "Fashion")
        , ('CO', "Communications")
        , ('FB', "Food and Beverage")
        , ('RE', "Research")
        , ('OT', "Other")
                       ]
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CompanyForm(ModelForm):
    # name = forms.CharField(max_length=50)
    # companyLogo = models.ImageField(default="images/115x115.gif", verbose_name="Company Logo")
    # industry = forms.CharField(widget=forms.Select(choices=industryChoices))
    # typeOfBusiness = forms.CharField(max_length=50)
    # website = forms.URLField()
    # phone = forms.IntegerField()
    class Meta:
        model = Company
        fields = ('name', 'email', 'industry', 'typeOfBusiness', 'website', 'phone', 'companyLogo')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = "__all__"

        """
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
            'duration' : forms.TextInput(attrs={'class': 'form-control'}),
            'location' : forms.TextInput(attrs={'class': 'form-control'}),
            'startDate' : forms.DateField(attrs={'class': 'form-control'}),
            'qualification' : forms.TextInput(attrs={'class': 'form-control'}),
            'stipend' : forms.BooleanField(),
            'description' : forms.Textarea(attrs={'class': 'form-control'}),
            'requirements' : forms.Textarea(attrs={'class': 'form-control'}),
        }
        """


class ApplyForm(forms.ModelForm):
    class Meta:
        model = Apply
        fields = "__all__"

