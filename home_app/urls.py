from django.conf.urls import url
from django.views.generic import RedirectView
from home_app.views import *

urlpatterns = [
    url(r'^home/$', homepage, name='home_app_home'),
    url(r'^$', RedirectView.as_view(url='home')),
]