from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .coordinator_exit_model_wrapper import CoordinatorExitModelWrapper


class CoordinatorExitModelWrapperMixin:

    coordinator_exit_model_wrapper_cls = CoordinatorExitModelWrapper

    @property
    def coordinator_exit_model_obj(self):
        """Returns a coordinator exit model instance or None.
        """
        try:
            return self.coordinator_exit_cls.objects.get(**self.coordinator_exit_options)
        except ObjectDoesNotExist:
            return None

    @property
    def coordinator_exit(self):
        """Returns a wrapped saved or unsaved coordinator exit.
        """
        model_obj = self.coordinator_exit_model_obj or self.coordinator_exit_cls(
            **self.create_coordinator_exit_options)
        return self.coordinator_exit_model_wrapper_cls(model_obj=model_obj)

    @property
    def coordinator_exit_cls(self):
        return django_apps.get_model('potlako_prn.coordinatorexit')

    @property
    def create_coordinator_exit_options(self):
        """Returns a dictionary of options to create a new
        unpersisted coordinator exit model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def coordinator_exit_options(self):
        """Returns a dictionary of options to get an existing
        coordinator exit model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options
