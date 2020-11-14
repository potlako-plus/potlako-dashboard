from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .special_forms_model_wrapper import SpecialFormsModelWrapper


class CancerDxEndpointModelWrapperMixin:

    cancer_dx_endpoint_model_wrapper_cls = SpecialFormsModelWrapper

    @property
    def cancer_dx_endpoint_model_obj(self):
        """Returns a cancer diagnosis and treatment endpoint model 
        instance or None.
        """
        try:
            return self.cancer_dx_endpoint_cls.objects.get(
                **self.cancer_dx_endpoint_options)
        except ObjectDoesNotExist:
            return None

    @property
    def cancer_dx_endpoint(self):
        """Returns a wrapped saved or unsaved baseline clinical summary .
        """
        model_obj = self.cancer_dx_endpoint_model_obj or self.cancer_dx_endpoint_cls(
            **self.create_cancer_dx_endpoint_options)
        return self.cancer_dx_endpoint_model_wrapper_cls(model_obj=model_obj)

    @property
    def cancer_dx_endpoint_cls(self):
        return django_apps.get_model('potlako_subject.cancerdxandtxendpoint')

    @property
    def create_cancer_dx_endpoint_options(self):
        """Returns a dictionary of options to create a new
        unpersisted cancer diagnosis and treatment endpoint model instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options

    @property
    def cancer_dx_endpoint_options(self):
        """Returns a dictionary of options to get an existing
        cancer diagnosis and treatment endpoint instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options
