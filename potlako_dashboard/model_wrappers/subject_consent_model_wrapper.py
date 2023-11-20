from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from edc_model_wrapper import ModelWrapper

from .baseline_summary_model_wrapper_mixin import BaselineClinicalSummaryModelWrapperMixin
from .cancer_dx_endpoint_model_wrapper_mixin import CancerDxEndpointModelWrapperMixin
from .care_seeking_endpoint_model_wrapper_mixin import \
    CareSeekingEndpointModelWrapperMixin
from .coordinator_exit_wrapper_mixin import CoordinatorExitModelWrapperMixin
from .death_report_wrapper_mixin import DeathReportModelWrapperMixin
from .navigation_plan_summary_model_wrapper_mixin import \
    NavigationPlanSummaryModelWrapperMixin
from .offstudy_wrapper_mixin import OffstudyModelWrapperMixin
from .subject_locator_model_wrapper_mixin import SubjectLocatorModelWrapperMixin
from ..utils import determine_flag


class SubjectConsentModelWrapper(
        SubjectLocatorModelWrapperMixin,
        BaselineClinicalSummaryModelWrapperMixin,
        NavigationPlanSummaryModelWrapperMixin,
        CancerDxEndpointModelWrapperMixin,
        CareSeekingEndpointModelWrapperMixin,
        DeathReportModelWrapperMixin,
        OffstudyModelWrapperMixin,
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
        return determine_flag(self.subject_identifier)

    @property
    def subject_community(self):

        clinician_call_enrol_cls = django_apps.get_model(
            'potlako_subject.cliniciancallenrollment')

        try:
            clinician_enrollment_obj = clinician_call_enrol_cls.objects.get(
                screening_identifier=self.screening_identifier)
        except clinician_call_enrol_cls.DoesNotExist:
            raise ValidationError('Clinician Call Enrollment object '
                                  'does not exist.')
        else:
            facility_name = clinician_enrollment_obj.facility
            facility_name = facility_name.replace("_", " ")
            facility_name = facility_name.replace("hospital", "")
            facility_name = facility_name.replace("clinic", "").strip().title()
            return facility_name
