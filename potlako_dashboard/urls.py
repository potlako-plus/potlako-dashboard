"""potlako_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/"""

from django.conf import settings
from django.urls.conf import path, include
from edc_dashboard import UrlConfig

from .patterns import subject_identifier, screening_identifier
from .views import (
    SubjectListboardView, SubjectDashboardView,
    SubjectScreeningListboardView)

app_name = 'potlako_dashboard'

subject_listboard_url_config = UrlConfig(
    url_name='subject_listboard_url',
    view_class=SubjectListboardView,
    label='subject_listboard',
    identifier_label='subject_identifier',
    identifier_pattern=subject_identifier)

screening_listboard_url_config = UrlConfig(
    url_name='screening_listboard_url',
    view_class=SubjectScreeningListboardView,
    label='screening_listboard',
    identifier_label='screening_identifier',
    identifier_pattern=screening_identifier)

subject_dashboard_url_config = UrlConfig(
    url_name='subject_dashboard_url',
    view_class=SubjectDashboardView,
    label='subject_dashboard',
    identifier_label='subject_identifier',
    identifier_pattern=subject_identifier)

urlpatterns = []
urlpatterns += subject_listboard_url_config.listboard_urls
urlpatterns += screening_listboard_url_config.listboard_urls
urlpatterns += subject_dashboard_url_config.dashboard_urls

if settings.APP_NAME == 'potlako_dashboard':

    from django.views.generic.base import RedirectView

    urlpatterns += [
        path('accounts/', include('edc_base.auth.urls')),
        path('edc_data_manager/', include('edc_data_manager.urls')),
        path('edc_device/', include('edc_device.urls')),
        path('edc_protocol/', include('edc_protocol.urls')),
        path('admininistration/', RedirectView.as_view(url='admin/'),
             name='administration_url'),
        path(r'', RedirectView.as_view(url='admin/'), name='home_url')]
