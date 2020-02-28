from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .subject_screening_model_wrapper import SubjectScreeningModelWrapper


class SubjectScreeningModelWrapperMixin:

    subject_screening_model_wrapper_cls = SubjectScreeningModelWrapper

    @property
    def subject_screening_model_obj(self):
        """Returns a subject screening model instance or None.
        """
        try:
            return self.subject_screening_cls.objects.get(
                **self.subject_screening_options)
        except ObjectDoesNotExist:
            return None

    @property
    def subject_screening(self):
        """Returns a wrapped saved or unsaved subject screening.
        """
        model_obj = self.subject_screening_model_obj or self.subject_screening_cls(
            **self.subject_screening_options)
        return self.subject_screening_model_wrapper_cls(model_obj=model_obj)

    @property
    def subject_screening_cls(self):
        return django_apps.get_model('potlako_subject.subjectscreening')

    @property
    def subject_screening_options(self):
        """Returns a dictionary of options to get an existing
        specimen consent model instance.
        """
        options = dict(
            screening_identifier=self.object.screening_identifier)
        return options
