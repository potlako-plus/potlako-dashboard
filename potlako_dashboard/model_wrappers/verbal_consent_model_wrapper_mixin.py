from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .verbal_consent_model_wrapper import VerbalConsentModelWrapper
from ..views.screening.pdf_response_mixin import PdfResponseMixin


class VerbalConsentModelWrapperMixin(PdfResponseMixin):

    verbal_consent_model_wrapper_cls = VerbalConsentModelWrapper

    @property
    def verbal_consent_model_obj(self):
        """Returns a verbal consent model instance or None.
        """
        try:
            return self.verbal_consent_cls.objects.get(
                **self.verbal_consent_options)
        except ObjectDoesNotExist:
            return None

    @property
    def verbal_consent(self):
        """Returns a wrapped saved or unsaved verbal consent.
        """
        model_obj = self.verbal_consent_model_obj or self.verbal_consent_cls(
            **self.verbal_consent_options)
        return self.verbal_consent_model_wrapper_cls(model_obj=model_obj)

    @property
    def verbal_consent_cls(self):
        return django_apps.get_model('potlako_subject.verbalconsent')

    @property
    def verbal_consent_options(self):
        """Returns a dictionary of options to get an existing
        verbal consent model instance.
        """
        options = dict(
            screening_identifier=self.object.screening_identifier,
            )
        return options
