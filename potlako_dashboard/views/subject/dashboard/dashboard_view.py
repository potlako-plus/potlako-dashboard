from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from edc_action_item.site_action_items import site_action_items
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.views import DashboardView as BaseDashboardView
from edc_navbar import NavbarViewMixin
from edc_subject_dashboard.view_mixins import SubjectDashboardViewMixin

from potlako_subject.action_items import SUBJECT_LOCATOR_ACTION

from ....model_wrappers import (
    AppointmentModelWrapper, SubjectConsentModelWrapper,
    SpecialFormsModelWrapper, SubjectVisitModelWrapper)


class DashboardView(EdcBaseViewMixin, SubjectDashboardViewMixin,
                    NavbarViewMixin, BaseDashboardView):

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
                    'visit_code')
        return self._appointments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        locator_obj = self.get_locator_info()
        context.update(
            locator_obj=locator_obj,
            community_arm=self.community_arm,
            subject_consent=self.consent_wrapped)
        return context

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

        if not obj:
            action_cls = site_action_items.get(
                self.subject_locator_model_cls.action_name)
            action_item_model_cls = action_cls.action_item_model_cls()
            try:
                action_item_model_cls.objects.get(
                    subject_identifier=subject_identifier,
                    action_type__name=SUBJECT_LOCATOR_ACTION)
            except ObjectDoesNotExist:
                action_cls(
                    subject_identifier=subject_identifier)
        return obj

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
    def community_arm(self):
        onschedule_model_cls = django_apps.get_model(
            'potlako_subject.onschedule')
        subject_identifier = self.kwargs.get('subject_identifier')
        try:
            onschedule_obj = onschedule_model_cls.objects.get(
                subject_identifier=subject_identifier)
        except ObjectDoesNotExist:
            return None
        else:
            return onschedule_obj.community_arm
