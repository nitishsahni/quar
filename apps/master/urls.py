from django.urls import path
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    # the home page
    path('', views.home, name='home'),
    # the application page
    path('internships/apply/<int:post_id>', views.apply, name='apply'),
    # the internships list
    path('internships', views.internships, name='internships'),
    # the single internship
    path('internships/<int:post_id>', views.singleInternship, name='singleInternship'),
    # the about page
    path('about', views.about, name="about"),
    # the post form page
    path('post', views.post, name="post"),
    # the track internship page
    path('track/<int:apply_id>', views.track, name="track"),

    url(r'^login/$', auth_views.LoginView, name='login'),

    path('logout', auth_views.LogoutView, {'next_page': 'home.html'}, name='logout'),

    path('signup', views.signup, name='signup'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        views.activate, name='activate'),



]