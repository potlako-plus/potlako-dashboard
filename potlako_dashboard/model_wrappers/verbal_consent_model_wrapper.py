from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_model_wrapper import ModelWrapper
from edc_consent.model_wrappers import ConsentModelWrapperMixin


class VerbalConsentModelWrapper(ConsentModelWrapperMixin, ModelWrapper):

    model = 'potlako_subject.verbalconsent'
    querystring_attrs = ['screening_identifier', 'language']
    next_url_attrs = ['screening_identifier', 'language']
#     next_url_name = 'add_consent_href'

    @property
    def next_url_name(self):
        return self.consent.href
    

    @property
    def verbal_consent_model_obj(self):
        """Returns a verbal consent model instance or None.
        """
        try:
            return self.object.verbalconsent_set.get(**self.consent_options)
        except ObjectDoesNotExist:
            return None

    @property
    def verbal_consent(self):
        """Returns a wrapped saved or unsaved verbal consent.
        """
        model_obj = self.verbal_consent_model_obj or self.verbal_consent_cls(
            **self.create_consent_options)
        return self(model_obj=model_obj)
    
    @property
    def verbal_consent_cls(self):
        return django_apps.get_model('potlako_subject.verbalconsent')

    @property
    def create_Verbal_consent_options(self):
        """Returns a dictionary of options to create a new
        unpersisted verbal consent model instance.
        """
        options = dict(
            screening_identifier=self.object.screening_identifier,
            version=self.consent_object.version)
        return options

    @property
    def verbal_consent_options(self):
        """Returns a dictionary of options to get an existing
        verbal consent model instance.
        """
        options = dict(
            screening_identifier=self.object.screening_identifier,
            version=self.consent_object.version)
        return options
