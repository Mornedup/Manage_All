from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^uploaddoc/$', views.upload_doc, name='upload_doc'),
    url(r'^doclist/$', views.view_doclist, name='doc_list'),
    url(r'^(?P<pk>\d+)/$', views.view_doc, name='view_doc'),
]
