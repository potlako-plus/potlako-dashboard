from django.conf import settings
from edc_navbar import NavbarItem, site_navbars, Navbar


no_url_namespace = True if settings.APP_NAME == 'potlako_dashboard' else False

potlako_dashboard = Navbar(name='potlako_dashboard')

potlako_dashboard.append_item(
    NavbarItem(
        name='eligible_subject',
        title='Subject Screening',
        label='Subject Screening',
        fa_icon='fa fa-user-plus',
        url_name=settings.DASHBOARD_URL_NAMES[
            'screening_listboard_url'],
        no_url_namespace=no_url_namespace))

potlako_dashboard.append_item(
    NavbarItem(
        name='consented_subject',
        title='Potlako Subjects',
        label='potlako subjects',
        fa_icon='far fa-user-circle',
        url_name=settings.DASHBOARD_URL_NAMES['subject_listboard_url'],
        no_url_namespace=no_url_namespace))

potlako_dashboard.append_item(
    NavbarItem(
        name='endpoint_recordings',
        title='Endpoint Recordings',
        label='endpoint recordings',
        fa_icon='far fa-user-circle',
        url_name=settings.DASHBOARD_URL_NAMES['endpoint_listboard_url'],
        no_url_namespace=no_url_namespace))

site_navbars.register(potlako_dashboard)
