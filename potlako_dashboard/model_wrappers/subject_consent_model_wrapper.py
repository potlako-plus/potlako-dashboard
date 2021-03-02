from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from edc_base.utils import age, get_utcnow

from edc_appointment.constants import COMPLETE_APPT
from edc_model_wrapper import ModelWrapper
from .subject_locator_model_wrapper_mixin import SubjectLocatorModelWrapperMixin
from .baseline_summary_model_wrapper_mixin import BaselineClinicalSummaryModelWrapperMixin
from .navigation_plan_summary_model_wrapper_mixin import NavigationPlanSummaryModelWrapperMixin
from .cancer_dx_endpoint_model_wrapper_mixin import CancerDxEndpointModelWrapperMixin
from .care_seeking_endpoint_model_wrapper_mixin import CareSeekingEndpointModelWrapperMixin


class SubjectConsentModelWrapper(
        SubjectLocatorModelWrapperMixin,
        BaselineClinicalSummaryModelWrapperMixin,
        NavigationPlanSummaryModelWrapperMixin,
        CancerDxEndpointModelWrapperMixin,
        CareSeekingEndpointModelWrapperMixin,
        ModelWrapper):

    model = 'potlako_subject.subjectconsent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get('subject_listboard_url')
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['screening_identifier', 'subject_identifier',
                         'first_name', 'last_name', 'language']

    @property
    def verbal_consent_obj(self):
        verbal_consent_cls = django_apps.get_model('potlako_subject.verbalconsent')
        try:
            return verbal_consent_cls.objects.get(
                screening_identifier=self.screening_identifier,
                version='1')
        except ObjectDoesNotExist:
            return None

    @property
    def verbal_consent_pdf_url(self):
        if self.verbal_consent_obj:
            return self.verbal_consent_obj.file.url
        return None
