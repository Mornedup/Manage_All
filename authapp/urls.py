from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', auth_views.logout,  {'next_page': 'homepage'}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^changepassword/$', views.change_password, name='change_password'),
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
]
