from django.conf.urls import url
from django.views.generic import RedirectView
from apps.finance_share_app import views

urlpatterns = [
    url(r'^manage_claims/$', views.manage_claims_view, name='manage_claims'),
    url(r'^report_select/$', views.report_select, name='report_select'),
    url(r'^report/$', views.last_month_report, name='last_month_report'),
    url(r'^report2/$', views.current_month_report, name='current_month_report'),
    url(r'^home/$', views.finance_share_home, name='finance_share_home'),
    url(r'^view_claim/(?P<document_pk>\d+)/$', views.view_claim, name='view_claim'),
    url(r'^upload_new_claim', views.upload_new_claim, name='upload_new_claim'),
    url(r'^add_claim/(?P<document_pk>\d+)/$', views.add_claim, name='add_claim'),
    url(r'^edit_claim/(?P<document_pk>\d+)/(?P<claim_pk>\d+)/$', views.edit_claim, name='edit_claim'),
    url(r'^info_claim/(?P<claim_pk>\d+)/$', views.info_claim, name='info_claim'),
    url(r'^overview/(?P<owe_to>[-\w]+)/(?P<daterange>[-\w]+)/$', views.overview, name='overview'),
    url(r'^$', RedirectView.as_view(url='finance_share_home')),
]