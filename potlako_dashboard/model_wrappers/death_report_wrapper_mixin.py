from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .death_report_model_wrapper import DeathReportModelWrapper


class DeathReportModelWrapperMixin:

    death_report_model_wrapper_cls = DeathReportModelWrapper

    @property
    def death_report_model_obj(self):
        """Returns a death model instance or None.
        """
        try:
            return self.death_report_cls.objects.get(**self.death_report_options)
        except ObjectDoesNotExist:
            return None

    @property
    def death_report(self):
        """Returns a wrapped saved or unsaved death report.
        """
        model_obj = self.death_report_model_obj or self.death_report_cls(
            **self.create_death_report_options)
        return self.death_report_model_wrapper_cls(model_obj=model_obj)

    @property
    def death_report_cls(self):
        return django_apps.get_model('potlako_prn.deathreport')

    @property
    def create_death_report_options(self):
        """Returns a dictionary of options to create a new
        unpersisted death report model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def death_report_options(self):
        """Returns a dictionary of options to get an existing
        death report model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options
