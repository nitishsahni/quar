from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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
from django.template import RequestContext



def home(request):
    return render(request, 'home.html')


@login_required
def post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            post.save()
            return HttpResponse('Thank you for posting')
    else:
        form = PostForm()
    return render(request, 'company/post.html', {'form': form})

def apply(request, post_id):
    postObj = get_object_or_404(Post, pk=post_id)
    form = ApplyForm(request.POST, request.FILES, initial={'post': postObj, })
    if request.method == 'POST':
        if form.is_valid():
            application = form.save(commit=False)
            application.save()
            #Send mail
            applyTo = form.cleaned_data.get('post.company')
            emailTo = form.cleaned_data.get('student.email')
            subject = 'Thank you for applying to ' + applyTo
            message = 'Now, you can track your internship application with the link quar.in/track/' + application.id
            recepient = emailTo
            EmailMessage(subject, message, to=recepient)
            return HttpResponse('Thank you for applying')
    else:
        form = ApplyForm(request.POST, request.FILES, initial={'post': postObj, })
    return render(request, 'student/apply.html', {'form': form, 'post': postObj})

def internships(request):
    latest_internship_list = Post.objects.all().order_by("-pk")
    context = {'latest_internship_list': latest_internship_list}
    return render(request, 'student/internships.html', context)


def singleInternship(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'student/singleInternship.html', {'post': post})


def about(request):
    return render(request, 'about.html')


def signup(request):
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
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
        company_form = CompanyForm(request.POST, request.FILES)
    return render(request, 'signups/companyregister.html', {'form': form, 'companyform' : company_form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

@login_required
def companyDashboard(request):
    return render(request, 'company/companydashboard.html')


def track(request, apply_id):
    apply = get_object_or_404(Apply, pk=apply_id)
    return render(request, 'student/track.html', {'applyStatus': apply.status, 'applyName': apply.student.name})

@login_required
def appliedDashboard(request):
    applications = Apply.objects.filter(post__company__email=request.user.email)
    applications_dict = {'applications' : applications}
    return render(request, 'company/viewApplied.html', applications_dict)

@login_required
def postedDashboard(request):
    posts = Post.objects.filter(company_id=request.user.company.id)
    posts_dict = {'posts' : posts}
    return render(request, 'company/viewPast.html', posts_dict)

@login_required
def viewAppDetails(request, apply_id):
    apply = get_object_or_404(Apply, pk=apply_id)
    return render(request, 'company/appDetails.html', {'apply' : apply})

@login_required
def companyDetail(request):
    context = {}
    context["form"] = Company.objects.get(id=request.user.company.id)
    return render(request, "company/companyEditProfile.html", context)


@login_required
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