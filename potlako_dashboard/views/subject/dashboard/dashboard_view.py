from django.apps import apps as django_apps
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.exceptions import ObjectDoesNotExist
from edc_action_item.site_action_items import site_action_items
from edc_base.view_mixins import EdcBaseViewMixin
from edc_constants.constants import DONE, NEW, OPEN, CLOSED
from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_navbar import NavbarViewMixin
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin

from potlako_subject.action_items import SUBJECT_LOCATOR_ACTION
from .navigation_history_mixin import NavigationHistoryMixin
from ....model_wrappers import (AppointmentModelWrapper,
                                ClinicianCallEnrollmentModelWrapper,
                                SpecialFormsModelWrapper, SubjectConsentModelWrapper,
                                SubjectVisitModelWrapper)
from ....utils import community_arm, determine_flag


class DashboardView(EdcBaseViewMixin, SubjectDashboardViewMixin, NavbarViewMixin,
                    BaseDashboardView, NavigationHistoryMixin):
    dashboard_url = 'subject_dashboard_url'
    dashboard_template = 'subject_dashboard_template'
    appointment_model = 'edc_appointment.appointment'
    appointment_model_wrapper_cls = AppointmentModelWrapper
    consent_model = 'potlako_subject.subjectconsent'
    consent_model_wrapper_cls = SubjectConsentModelWrapper
    navbar_name = 'potlako_dashboard'
    navbar_selected_item = 'consented_subject'
    subject_locator_model = 'potlako_subject.subjectlocator'
    subject_locator_model_wrapper_cls = SpecialFormsModelWrapper
    visit_model_wrapper_cls = SubjectVisitModelWrapper
    special_forms_include_value = "potlako_dashboard/subject/dashboard/special_forms.html"
    data_action_item_template = "potlako_dashboard/subject/dashboard/data_manager.html"

    @property
    def appointments(self):
        """Returns a Queryset of all appointments for this subject.
        """
        if not self._appointments:
            self._appointments = self.appointment_model_cls.objects.filter(
                subject_identifier=self.subject_identifier).order_by(
                'visit_code', 'visit_code_sequence')
        return self._appointments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.create_nav_plan_actions()
        locator_obj = self.get_subject_locator_or_message()
        edc_readonly = None

        if self.request.GET.get('edc_readonly'):
            edc_readonly = self.request.GET.get('edc_readonly') == '1'

        # Ignore error messages if readonly view
        if edc_readonly:
            storage = get_messages(self.request)
            storage.used = True

        context.update(
            locator_obj=locator_obj,
            community_arm=community_arm(self.subject_identifier),
            participant_exit=self.participant_exit,
            subject_consent=self.consent_wrapped,
            clinician_call_enrol=ClinicianCallEnrollmentModelWrapper(
                self.clinician_call_enrol_obj()),
            groups=[g.name for g in self.request.user.groups.all()],
            nav_flag=determine_flag(self.subject_identifier),
            open_action_items=self.open_action_items,
            edc_readonly=edc_readonly,
            hiv_status=self.get_hiv_status,
            navigation_plans=self.navigation_plan_history_objs,
            navigation_plan_inlines=self.navigation_plan_inlines,
            current_navigation_plan=self.current_navigation_plan,
            current_navigation_plan_inlines=self.current_navigation_plan_inlines,
            evaluation_timeline_history=self.evaluation_timelines_history_objs)
        return context

    def message_user(self, message=None):
        if (not self.request.GET.get('edc_readonly')
                or self.request.GET.get('edc_readonly') != '1'):
            messages.error(self.request, message=message)

    @property
    def get_hiv_status(self):
        patient_initial = django_apps.get_model(
            'potlako_subject.patientcallinitial')

        try:
            patient_initial_obj = patient_initial.objects.get(
                subject_visit__subject_identifier=self.kwargs.get('subject_identifier'))
        except patient_initial.DoesNotExist:
            if self.clinician_call_enrol_obj():
                return self.clinician_call_enrol_obj().last_hiv_result
        else:
            return patient_initial_obj.hiv_status

    def clinician_call_enrol_obj(self):

        enrolmment_model = django_apps.get_model(
            'potlako_subject.cliniciancallenrollment')
        try:
            enrolmment_model_obj = enrolmment_model.objects.get(
                screening_identifier=self.consent_wrapped.screening_identifier)
        except enrolmment_model.DoesNotExist:
            return None
        else:
            return enrolmment_model_obj

    def get_locator_info(self):

        subject_identifier = self.kwargs.get('subject_identifier')
        try:
            obj = self.subject_locator_model_cls.objects.get(
                subject_identifier=subject_identifier)
        except ObjectDoesNotExist:
            return None
        return obj

    def get_subject_locator_or_message(self):
        obj = self.get_locator_info()
        subject_identifier = self.kwargs.get('subject_identifier')

        query_options = {
            'subject_identifier': subject_identifier,
            'action_type__name': SUBJECT_LOCATOR_ACTION}
        if obj:
            query_options.update(
                {'action_identifier': obj.action_identifier})

        action_cls = site_action_items.get(
            self.subject_locator_model_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()
        try:
            locator_item = action_item_model_cls.objects.get(
                **query_options)
        except action_item_model_cls.DoesNotExist:
            locator_item = action_cls(
                subject_identifier=subject_identifier).action_item_obj

        if obj:
            if obj.action_identifier != locator_item.action_identifier:
                # Update locator obj action_identifier if action item queried
                # does not match locator action.
                obj.action_identifier = locator_item.action_identifier
                obj.save()
            if locator_item.status in [OPEN, NEW]:
                # Update action item status to close the action item if OPEN.
                locator_item.status = CLOSED
                locator_item.save()
        return obj

    def create_nav_plan_actions(self):
        """Create navigation plan actions.
        """
        subject_identifier = self.kwargs.get('subject_identifier')
        nav_plan_model_cls = django_apps.get_model(
            'potlako_subject.navigationsummaryandplan')
        action_cls = site_action_items.get(nav_plan_model_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()

        complete_apps = self.appointments.filter(
            appt_status=DONE, visit_code__in=['2000', '3000']).count()

        nav_plan_actions = action_item_model_cls.objects.filter(
            subject_identifier=subject_identifier).exclude(
            status__in=[NEW, OPEN]).count()

        if complete_apps > nav_plan_actions < 1 and 'Standard' in community_arm(
                subject_identifier):
            action_cls(
                subject_identifier=subject_identifier)

    def action_cls_item_creator(
            self, subject_identifier=None, action_cls=None, action_type=None):
        action_cls = site_action_items.get(
            action_cls.action_name)
        action_item_model_cls = action_cls.action_item_model_cls()
        try:
            action_item_model_cls.objects.get(
                subject_identifier=subject_identifier,
                action_type__name=action_type)
        except ObjectDoesNotExist:
            action_cls(
                subject_identifier=subject_identifier)

    @property
    def participant_exit(self):
        exit_model_cls = django_apps.get_model(
            'potlako_subject.cancerdxandtxendpoint')
        subject_identifier = self.kwargs.get('subject_identifier')
        final_deposition = 'exit'
        try:
            exit_obj = exit_model_cls.objects.get(
                subject_identifier=subject_identifier, final_deposition=final_deposition)
        except ObjectDoesNotExist:
            return None
        else:
            return exit_obj.final_deposition
