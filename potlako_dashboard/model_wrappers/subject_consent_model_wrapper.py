from django.conf import settings
from edc_model_wrapper import ModelWrapper


class SubjectConsentModelWrapper(ModelWrapper):

    model = 'potlako_subject.subjectconsent'
    next_url_name = settings.DASHBOARD_URL_NAMES.get('screening_listboard_url')
    next_url_attrs = ['screening_identifier']
    querystring_attrs = ['screening_identifier', 'subject_identifier']
