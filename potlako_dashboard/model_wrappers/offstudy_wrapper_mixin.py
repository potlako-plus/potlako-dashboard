from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .offstudy_model_wrapper import OffstudyModelWrapper


class OffstudyModelWrapperMixin:

    offstudy_model_wrapper_cls = OffstudyModelWrapper

    @property
    def offstudy_model_obj(self):
        """Returns a subject offstudy instance or None.
        """
        try:
            return self.offstudy_cls.objects.get(**self.offstudy_options)
        except ObjectDoesNotExist:
            return None

    @property
    def offstudy(self):
        """Returns a wrapped saved or unsaved subject offstudy instance.
        """
        model_obj = self.offstudy_model_obj or self.offstudy_cls(
            **self.create_offstudy_options)
        return self.offstudy_model_wrapper_cls(model_obj=model_obj)

    @property
    def offstudy_cls(self):
        return django_apps.get_model('potlako_prn.subjectoffstudy')

    @property
    def create_offstudy_options(self):
        """Returns a dictionary of options to create a new
        unpersisted offstudy model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options

    @property
    def offstudy_options(self):
        """Returns a dictionary of options to get an existing
        death report model instance.
        """
        options = dict(
            subject_identifier=self.object.subject_identifier)
        return options
