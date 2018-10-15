from django.conf.urls import url
from django.views.generic import RedirectView
from home_app.views import *

urlpatterns = [
    url(r'^homepage/$', homepage, name='homepage'),
    url(r'^$', RedirectView.as_view(url='homepage')),
]