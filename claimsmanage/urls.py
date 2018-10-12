from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^uploadclaim/$', views.makeclaim, name='upload_claim'),
    url(r'^listclaims/$', views.view_claimslist, name='claims_list'),
    url(r'^(?P<pk>\d+)/$', views.view_claim, name='view_claim'),
]
