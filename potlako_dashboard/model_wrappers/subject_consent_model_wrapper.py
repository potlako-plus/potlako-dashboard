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

    @property
    def last_appointment_date(self):
        patient_initial_cls = django_apps.get_model('potlako_subject.patientcallinitial')
        patient_fu_cls = django_apps.get_model('potlako_subject.patientcallfollowup')
        clinician_enrollment_cls = django_apps.get_model('potlako_subject.cliniciancallenrollment')

        patient_call_obj = patient_fu_cls.objects.filter(
                                     subject_visit__subject_identifier=self.object.subject_identifier).order_by('-created')

        if not patient_call_obj:
            try:
                patient_call_obj = patient_initial_cls.objects.filter(
                                            subject_visit__subject_identifier=self.object.subject_identifier).order_by('-created')
            except patient_initial_cls.DoesNotExist:
                try:
                    clinician_enrollment_obj = clinician_enrollment_cls.objects.get(
                                        screening_identifier=self.object.screening_identifier)
                except clinician_enrollment_cls.DoesNotExist:
                    raise
                else:
                    return clinician_enrollment_obj.referral_date

        if patient_call_obj:
            return patient_call_obj[0].next_appointment_date
        return None

    @property
    def initial_visit_complete(self):
        subject_visit_cls = django_apps.get_model('potlako_subject.subjectvisit')

        initial_visit_obj = subject_visit_cls.objects.filter(
            appointment__visit_code=1000).filter(appointment__appt_status=COMPLETE_APPT)

        if initial_visit_obj:
            return initial_visit_obj
        return None

    @property
    def worklist_ready(self):
        if self.last_appointment_date:
            return self.last_appointment_date < get_utcnow().date()
        return False

    @property
    def cancer_probability(self):
        baseline_cls = django_apps.get_model('potlako_subject.baselineclinicalsummary')

        try:
            baseline_obj = baseline_cls.objects.get(subject_identifier=self.object.subject_identifier)
        except baseline_cls.DoesNotExist:
            return None
        else:
            return baseline_obj.cancer_concern or baseline_obj.cancer_concern_other

    @property
    def age_in_years(self):
        return age(self.object.dob, get_utcnow()).years

    @property
    def contacts(self):
        subject_locator_cls = django_apps.get_model('potlako_subject.subjectlocator')
        try:
            subject_locator_obj = subject_locator_cls.objects.get(
                subject_identifier=self.object.subject_identifier)
        except ObjectDoesNotExist:
            return None
        else:
            contacts = ('' + subject_locator_obj.subject_cell + '' +
                        subject_locator_obj.subject_cell_alt + '' +
                        subject_locator_obj.subject_phone + '' +
                        subject_locator_obj.subject_phone_alt)
            return contacts



