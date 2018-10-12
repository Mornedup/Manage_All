from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.reportselect, name='report_select'),
    url(r'^report/$',views.lastmonthreport, name='lastmonthreport'),
    url(r'^report/$',views.currentmonthreport, name='currentmonthreport'),
]
