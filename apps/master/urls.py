from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    # the home page
    path('', views.home, name='home'),
    # the internships list
    path('internships', views.internships, name='internships'),
    # the single internship
    path('internships/<int:post_id>', views.singleInternship, name='singleInternship'),
    # the about page
    path('about', views.about, name="about"),
    # the track internship page
    path('login', views.loginView, name='login'),

    path('logout', views.logoutView, name='logout'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        views.activate, name='activate'),



    path('companysignup', views.companySignup, name='companysignup'),

    path ('checkmail', views.checkMail, name='checkmail'),

    path('post', views.post, name="post"),

    path('companydashboard', views.companyDashboard, name="companydashboard"),

    path('companyappliedDashboard', views.appliedDashboard, name="companyappliedDashboard"),

    path('companypostedDashboard', views.postedDashboard, name="companypostedDashboard"),

    path('companyeditPost/<int:post_id>', views.editSinglePost, name="companyeditPost"),

    path('companyappDetails/<int:apply_id>', views.companyViewAppDetails, name="companyappDetails"),

    path('companyeditProfile', views.companyEditProfile, name='companyeditProfile'),

    path('companydetailProfile', views.companyDetail, name='companydetailProfile'),



    path('studentsignup', views.signupStudent, name='studentsignup'),

    path('apply/<int:post_id>', views.apply, name='apply'),

    path('studentdashboard', views.studentDashboard, name="studentdashboard"),

    path('studentappliedDashboard', views.studentApplied, name="studentappliedDashboard"),

    path('studenttrack/<int:apply_id>', views.track, name="studenttrack"),

    path('studentappDetails/<int:apply_id>', views.studentViewAppDetails, name="studentappDetails"),

    path('studenteditProfile', views.studentEditProfile, name='studenteditProfile'),

    path('studentdetailProfile', views.studentDetail, name='studentdetailProfile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
