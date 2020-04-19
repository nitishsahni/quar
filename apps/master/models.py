from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


class Student(models.Model):
    hs = 'HS'
    ba = 'BA'
    ma = 'MA'
    yearSchoolChoices = [(hs, 'High School'), (ba, 'Bachelors'), (ma, 'Masters')]

    name = models.CharField(max_length=50)
    email = models.EmailField()
    highSchool = models.CharField(verbose_name="High School", max_length=50)
    year = models.CharField(max_length=2, choices=yearSchoolChoices)
    dob = models.DateField()
    phone = models.BigIntegerField()

    def __str__(self):
        return self.name


class Company(models.Model):
    class Meta:
        verbose_name_plural = "Companies"

    industryChoices = [('FA', "Finance and Accounting"),
                       ('MA', "Marketing")
                        ,('DE', "Design")
                        ,('DS', "Data Analytics and Stats")
                        ,('PS', "Programming and Software")
                        ,('SC', "Supply Chain")
                        ,('FS', "Fashion")
                        ,('CO', "Communications")
                        ,('FB', "Food and Beverage")
                        ,('RE', "Research")
                        ,('OT', "Other")
                       ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="Company name")
    email = models.EmailField()
    industry = models.CharField(verbose_name="Industry", max_length=2, choices=industryChoices)
    typeOfBusiness = models.CharField(max_length=50, verbose_name="Type of Business")
    website = models.URLField()
    companyLogo = models.ImageField(default="images/115x115.gif", verbose_name="Company Logo", upload_to ='logos')
    phone = models.BigIntegerField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __str__(self):
        return self.name


class Post(models.Model):
    hs = 'HS'
    ba = 'BA'
    ma = 'MA'
    yearSchoolChoices = [(hs, 'High School'), (ba, 'Bachelors'), (ma, 'Masters')]

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    location = models.CharField(default="Remote", max_length=50)
    startDate = models.DateField(verbose_name="Start Date")
    qualification = models.CharField(max_length=2, choices=yearSchoolChoices)
    stipend = models.BooleanField()
    description = models.TextField(max_length=2000)
    requirements = models.TextField(max_length=2000)

    def __str__(self):
        return self.title


class Apply(models.Model):
    qr = 'QR'
    wc = 'WC'
    ap = 'AP'
    rj = "RJ"
    statusChoices = [(qr, 'Quar.in'), (wc, 'With company'), (ap, 'Approved'), (rj, 'Rejected')]

    hs = 'HS'
    ba = 'BA'
    ma = 'MA'
    yearSchoolChoices = [(hs, 'High School'), (ba, 'Bachelors'), (ma, 'Masters')]

    class Meta:
        verbose_name_plural = "Applications"

    name = models.CharField(max_length=50)
    email = models.EmailField()
    institution = models.CharField(verbose_name="High School", max_length=50)
    qualification = models.CharField(max_length=2, choices=yearSchoolChoices)
    dob = models.DateField()
    phone = models.BigIntegerField()
    #student = models.ForeignKey(Student, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resume/%Y/%m/%d')
    cover = models.FileField(null=True, upload_to='cover/%Y/%m/%d')
    skills = models.TextField(max_length=500)
    presence = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=statusChoices, default='QR')

    def __str__(self):
        return str(self.name) + " | " + str(self.post) + " | " + str(self.post.company)