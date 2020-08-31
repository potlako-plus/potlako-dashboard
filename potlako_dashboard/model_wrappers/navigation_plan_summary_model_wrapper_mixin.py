from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .special_forms_model_wrapper import SpecialFormsModelWrapper


class NavigationPlanSummaryModelWrapperMixin:

    navigation_plan_summary_model_wrapper_cls = SpecialFormsModelWrapper

    @property
    def navigation_plan_summary_model_obj(self):
        """Returns a navigation summary and plan model instance or None.
        """
        try:
            return self.navigation_plan_summary_cls.objects.get(
                **self.navigation_plan_summary_options)
        except ObjectDoesNotExist:
            return None

    @property
    def navigation_plan_summary(self):
        """Returns a wrapped saved or unsaved baseline clinical summary .
        """
        model_obj = self.navigation_plan_summary_model_obj or self.navigation_plan_summary_cls(
            **self.create_navigation_plan_summary_options)
        return self.navigation_plan_summary_model_wrapper_cls(model_obj=model_obj)

    @property
    def navigation_plan_summary_cls(self):
        return django_apps.get_model('potlako_subject.navigationsummaryandplan')

    @property
    def create_navigation_plan_summary_options(self):
        """Returns a dictionary of options to create a new
        unpersisted baseline clinical summary  model instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options

    @property
    def navigation_plan_summary_options(self):
        """Returns a dictionary of options to get an existing
        baseline clinical summary  instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options
