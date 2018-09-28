from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^uploadclaim/$', views.makeclaim, name='upload_claim'),
    url(r'^listclaims/$', views.view_claim, name='claims_list'),
]
