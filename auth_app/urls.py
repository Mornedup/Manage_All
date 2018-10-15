from django.conf.urls import url
from auth_app.views import *

urlpatterns = [
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^changepassword/$', change_password, name='change_password'),
    url(r'^profile/$', view_profile, name='view_profile'),
    url(r'^profile/edit/$', edit_profile, name='edit_profile'),
]
