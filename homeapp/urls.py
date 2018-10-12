from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^homepage/$', views.homepage, name='homepage'),
    url(r'^$', RedirectView.as_view(url='homepage')),

]
