from django.conf.urls import url
from finance_share_app import views

urlpatterns = [
    url(r'^uploaddoc/$', views.upload_document, name='upload_document'),
    url(r'^documentlist/$', views.view_document_list, name='document_list'),
    url(r'^view_document/(?P<pk>\d+)/$', views.view_document, name='view_document'),
    url(r'^uploadclaim/$', views.make_claim, name='upload_claim'),
    url(r'^listclaims/$', views.view_claim_list, name='claim_list'),
    url(r'^view_claim/(?P<pk>\d+)/$', views.view_claim, name='view_claim'),
    url(r'^report_select/$', views.report_select, name='report_select'),
    url(r'^report/$', views.last_month_report, name='last_month_report'),
    url(r'^report/$', views.current_month_report, name='current_month_report'),
    url(r'^home/', views.finance_share_home, name='finance_share_home')
]