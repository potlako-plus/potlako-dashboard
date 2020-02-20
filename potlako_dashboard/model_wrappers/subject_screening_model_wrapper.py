from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from edc_base.utils import formatted_age
from edc_consent import ConsentModelWrapperMixin
from edc_model_wrapper import ModelWrapper

from .subject_consent_model_wrapper import SubjectConsentModelWrapper


class SubjectScreeningModelWrapper(
        ConsentModelWrapperMixin,
        ModelWrapper):

    consent_model_wrapper_cls = SubjectConsentModelWrapper
    model = 'potlako_subject.subjectscreening'
    next_url_attrs = ['screening_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get('screening_listboard_url')

    @property
    def consented(self):
        return self.object.subject_identifier

    @property
    def create_consent_options(self):
        options = super().create_consent_options
        options.update(screening_identifier=self.object.screening_identifier)
        return options

    @property
    def consent_version(self):
        return '1'

    @property
    def consent_options(self):
        return dict(screening_identifier=self.object.screening_identifier)

    @property
    def consent_model_obj(self):
        consent_model_cls = django_apps.get_model(
            self.consent_model_wrapper_cls.model)
        try:
            return consent_model_cls.objects.get(**self.consent_options)
        except ObjectDoesNotExist:
            return None

    @property
    def age_in_years(self):

        if self.consent_model_obj:
            return formatted_age(self.consent_model_obj.dob)
        return None
