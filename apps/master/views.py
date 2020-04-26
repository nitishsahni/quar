from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .decorators import *



def home(request):
    return render(request, 'home.html')


def internships(request):
    latest_internship_list = Post.objects.all().order_by("-pk")
    context = {'latest_internship_list': latest_internship_list}
    return render(request, 'student/internships.html', context)


def singleInternship(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'student/singleInternship.html', {'post': post})


def about(request):
    return render(request, 'about.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.error(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid! Please try creating an account again.')
        return redirect('login')

def loginView(request):
    if request.user.is_authenticated:
        try:
            if request.user.company:
                return redirect('companydashboard')
        except Company.DoesNotExist:
            return redirect('studentdashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            try:
                if user.company:
                    return redirect('companydashboard')
            except Company.DoesNotExist:
                return redirect('studentdashboard')
        else:
            messages.error(request, 'Your username or password is incorrect.')
            return redirect('login')
    return render(request, 'signups/logIn.html')

def logoutView(request):
    logout(request)
    return redirect('home')

#####################

def companySignup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        company_form = CompanyForm(request.POST, request.FILES)
        if form.is_valid() and company_form.is_valid():
            user = form.save(commit=False)
            company = company_form.save(commit=False)
            user.is_active = False
            company.user = user
            user.save()
            company.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Quar.in account.'
            message = render_to_string('signups/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = company_form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'Thank you for registering! Check your email to authenticate your profile.')
            return redirect('login')
    else:
        form = SignupForm()
        company_form = CompanyForm()
    return render(request, 'signups/companyregister.html', {'form': form, 'companyform' : company_form})

@company_required
def companyDashboard(request):
    return render(request, 'company/companydashboard.html')

@company_required
def post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, {'company': request.user.company})
        if form.is_valid():
            post = form.save(commit=False)
            post.company = request.user.company
            post.save()
            messages.success(request, 'Congratulations on posting an internship!')
            return redirect('companydashboard')
    else:
        form = PostForm()
    return render(request, 'company/post.html', {'form': form})

@company_required
def appliedDashboard(request):
    applications = Apply.objects.filter(post__company=request.user.company)
    applications_dict = {'applications' : applications}
    return render(request, 'company/viewApplied.html', applications_dict)


@company_required
def postedDashboard(request):
    posts = Post.objects.filter(company_id=request.user.company.id)
    posts_dict = {'posts' : posts}
    return render(request, 'company/viewPast.html', posts_dict)

@company_required
def companyViewAppDetails(request, apply_id):
    apply = get_object_or_404(Apply, pk=apply_id)
    return render(request, 'company/appDetails.html', {'apply' : apply})

@company_required
def companyDetail(request):
    context = {}
    context["form"] = Company.objects.get(id=request.user.company.id)
    return render(request, "company/companyEditProfile.html", context)


@company_required
def companyEditProfile(request):
    context = {}
    obj = get_object_or_404(Company, id=request.user.company.id)

    changePasswordForm = PasswordChangeForm(request.user, request.POST or None)
    companyform = CompanyForm(request.POST or None, request.FILES or None, instance=obj)

    if changePasswordForm.is_valid():
        user = changePasswordForm.save()
        update_session_auth_hash(request, user)
        return HttpResponse("Your password has been changed.")

    if companyform.is_valid():
        companyform.save()
        return redirect('detail')

    context["companyform"] = companyform
    context["changePasswordForm"] = changePasswordForm

    return render(request, "company/companyEditProfile.html", context)

@company_required
def editSinglePost(request, post_id):
    context = {}
    obj = get_object_or_404(Post, id=post_id)

    form = PostForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return redirect('detail')

    context["form"] = form
    context["post_id"] = post_id

    return render(request, "company/editPost.html", context)


########
#########
#####

def signupStudent(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        student_form = StudentForm(request.POST)
        if form.is_valid() and student_form.is_valid():
            user = form.save(commit=False)
            student = student_form.save(commit=False)
            user.is_active = False
            student.user = user
            user.save()
            student.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Quar.in account.'
            message = render_to_string('signups/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = student_form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'Thank you for registering! Check your email to authenticate your profile.')
            return redirect('login')
    else:
        form = SignupForm()
        student_form = StudentForm()
    return render(request, 'signups/studentregister.html', {'form': form, 'studentform': student_form})

@student_required
def studentDashboard(request):
    return render(request, 'student/studentdashboard.html')

@student_required
def track(request, apply_id):
    apply = get_object_or_404(Apply, pk=apply_id)
    context = {}
    if (apply.status == "QR"):
        context['applyStatus'] = "is currently being reviewed by Quar.in"
    elif (apply.status == "WC"):
        context['applyStatus'] = "is currently being reviewed by " + apply.post.company.name
    elif (apply.status == "AP"):
        context['applyStatus'] = "has been approved! Congratulations! Reach out to" + apply.post.company.name + "!"
    elif (apply.status == "RJ"):
        context['applyStatus'] = "has been rejected! Congratulations! We're sorry"
    context['apply']  = apply
    return render(request, 'student/track.html', context)

@student_required
def studentApplied(request):
    applications = Apply.objects.filter(student = request.user.student)
    applications_dict = {'applications' : applications}
    return render(request, 'student/viewApplied.html', applications_dict)

@student_required
def studentViewAppDetails(request, apply_id):
    apply = get_object_or_404(Apply, pk=apply_id)
    form = ApplyForm(instance=apply)
    return render(request, 'student/appDetails.html', {'form' : form, 'apply': apply})

@student_required
def studentDetail(request):
    context = {}
    context["form"] = Student.objects.get(id=request.user.student.id)
    return render(request, "student/studentEditProfile.html", context)


@student_required
def studentEditProfile(request):
    context = {}
    obj = get_object_or_404(Student, id=request.user.student.id)

    changePasswordForm = PasswordChangeForm(request.user, request.POST or None)
    student_form = StudentForm(request.POST or None, request.FILES or None, instance=obj)

    if changePasswordForm.is_valid():
        user = changePasswordForm.save()
        update_session_auth_hash(request, user)
        return HttpResponse("Your password has been changed.")

    if student_form.is_valid():
        student_form.save()
        return redirect('detail')

    context["form"] = student_form
    context["changePasswordForm"] = changePasswordForm

    return render(request, "student/studentEditProfile.html", context)

@student_required
def apply(request, post_id):
    postObj = get_object_or_404(Post, pk=post_id)
    student = request.user.student
    form = ApplyForm(request.POST, request.FILES, {'post': postObj, 'student': student})
    if request.method == 'POST':
        if form.is_valid():
            application = form.save(commit=False)
            application.post = postObj
            application.student = student
            application.save()
            #Send mail
            applyTo = postObj.company.name
            emailTo = student.email
            subject = 'Thank you for applying to ' + applyTo
            message = render_to_string('student/apply_mail.html',{
                'name': request.user.student.name,
                'company': postObj.company.name,
                'post': postObj.title,
            })
            email = EmailMessage(subject, message, to=[emailTo])
            email.send()
            messages.success(request, 'Thank you for applying for your internship! You will hear back soon!')
            return redirect('studentdashboard')
    else:
        form = ApplyForm()
    return render(request, 'student/apply.html', {'form': form, 'post': postObj})