from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'potlako_dashboard'
    admin_site_name = 'potlako_subject_admin'
