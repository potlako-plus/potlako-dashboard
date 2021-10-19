from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from edc_base.utils import get_utcnow
from edc_constants.constants import NOT_DONE
from edc_model_wrapper import ModelWrapper

from .baseline_summary_model_wrapper_mixin import BaselineClinicalSummaryModelWrapperMixin
from .cancer_dx_endpoint_model_wrapper_mixin import CancerDxEndpointModelWrapperMixin
from .care_seeking_endpoint_model_wrapper_mixin import CareSeekingEndpointModelWrapperMixin
from .coordinator_exit_wrapper_mixin import CoordinatorExitModelWrapperMixin
from .death_report_wrapper_mixin import DeathReportModelWrapperMixin
from .navigation_plan_summary_model_wrapper_mixin import NavigationPlanSummaryModelWrapperMixin
from .subject_locator_model_wrapper_mixin import SubjectLocatorModelWrapperMixin


class SubjectConsentModelWrapper(
        SubjectLocatorModelWrapperMixin,
        BaselineClinicalSummaryModelWrapperMixin,
        NavigationPlanSummaryModelWrapperMixin,
        CancerDxEndpointModelWrapperMixin,
        CareSeekingEndpointModelWrapperMixin,
        DeathReportModelWrapperMixin,
        CoordinatorExitModelWrapperMixin,
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
    def language(self):
        if self.verbal_consent_obj:
            return self.verbal_consent_obj.language

    @property
    def verbal_consent_pdf_url(self):
        if self.verbal_consent_obj:
            return self.verbal_consent_obj.file.url
        return None

    @property
    def navigation_status(self):
        keysteps_form = django_apps.get_model('potlako_subject.evaluationtimeline')

        key_steps = keysteps_form.objects.filter(
            navigation_plan__subject_identifier=self.subject_identifier,
            key_step_status=NOT_DONE)
        flags = []

        for key_step in key_steps:
            today = get_utcnow().date()
            target_date = key_step.target_date

            if(today - target_date).days > 7:
                flags.append('past')
            elif (target_date - today).days > 7:
                flags.append('early')
            else:
                flags.append('on_time')

        flags = list(set(flags))
        return max(flags) if flags else 'default'
