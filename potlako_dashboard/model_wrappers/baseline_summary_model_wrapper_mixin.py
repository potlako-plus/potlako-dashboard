from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .baseline_summary_model_wrapper import BaselineClinicalSummaryModelWrapper


class BaselineClinicalSummaryModelWrapperMixin:

    baseline_summary_model_wrapper_cls = BaselineClinicalSummaryModelWrapper

    @property
    def baseline_summary_model_obj(self):
        """Returns a baseline clinical summary model instance or None.
        """
        try:
            return self.baseline_summary_cls.objects.get(
                **self.baseline_summary_options)
        except ObjectDoesNotExist:
            return None

    @property
    def baseline_summary(self):
        """Returns a wrapped saved or unsaved baseline clinical summary .
        """
        model_obj = self.baseline_summary_model_obj or self.baseline_summary_cls(
            **self.create_baseline_summary_options)
        return self.baseline_summary_model_wrapper_cls(model_obj=model_obj)

    @property
    def baseline_summary_cls(self):
        return django_apps.get_model('potlako_subject.baselineclinicalsummary')

    @property
    def create_baseline_summary_options(self):
        """Returns a dictionary of options to create a new
        unpersisted baseline clinical summary  model instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options

    @property
    def baseline_summary_options(self):
        """Returns a dictionary of options to get an existing
        baseline clinical summary  instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options
