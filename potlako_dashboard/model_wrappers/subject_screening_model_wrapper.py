from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from edc_model_wrapper import ModelWrapper

from edc_consent import ConsentModelWrapperMixin
from edc_consent.site_consents import site_consents

from .subject_consent_model_wrapper import SubjectConsentModelWrapper


class SubjectScreeningModelWrapper(
        ConsentModelWrapperMixin,
        ModelWrapper):

    consent_model_wrapper_cls = SubjectConsentModelWrapper
    model = 'potlako_subject.subjectscreening'
    next_url_attrs = ['screening_identifier', 'subject_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'screening_listboard_url')

    @property
    def consent_object(self):
        """Returns a consent configuration object from site_consents
        relative to the wrapper's "object" report_datetime.
        """
        default_consent_group = django_apps.get_app_config(
            'edc_consent').default_consent_group
        consent_object = site_consents.get_consent_for_period(
            model=self.consent_model_wrapper_cls.model,
            report_datetime=self.consent_version_model_obj.report_datetime,
            consent_group=default_consent_group,
            version=self.consent_version or None)

        return consent_object

    @property
    def consented(self):
        return self.object.subject_identifier

    @property
    def subject_identifier(self):
        return self.object.subject_identifier

    @property
    def create_consent_options(self):
        options = super().create_consent_options
        options.update(screening_identifier=self.object.screening_identifier)
        return options

    @property
    def consent_model_obj(self):
        consent_model_cls = django_apps.get_model(
            self.consent_model_wrapper_cls.model)
        try:
            return consent_model_cls.objects.get(**self.consent_options)
        except ObjectDoesNotExist:
            return None
