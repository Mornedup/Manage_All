from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^uploaddoc/$', views.upload_doc, name='upload_doc'),
    url(r'^doclist/$', views.view_doc, name='doc_list')
]
