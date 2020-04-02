from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .subject_locator_model_wrapper import SubjectLocatorModelWrapper


class SubjectLocatorModelWrapperMixin:

    subject_locator_model_wrapper_cls = SubjectLocatorModelWrapper

    @property
    def subject_locator_model_obj(self):
        """Returns a subject locator model instance or None.
        """
        try:
            return self.subject_locator_cls.objects.get(
                **self.subject_locator_options)
        except ObjectDoesNotExist:
            return None

    @property
    def subject_locator(self):
        """Returns a wrapped saved or unsaved subject locator.
        """
        model_obj = self.subject_locator_model_obj or self.subject_locator_cls(
            **self.create_subject_locator_options)
        return self.subject_locator_model_wrapper_cls(model_obj=model_obj)

    @property
    def subject_locator_cls(self):
        return django_apps.get_model('potlako_subject.subjectlocator')

    @property
    def create_subject_locator_options(self):
        """Returns a dictionary of options to create a new
        unpersisted subject locator model instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options

    @property
    def subject_locator_options(self):
        """Returns a dictionary of options to get an existing
        subject locator instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options
