from django.conf import settings
from edc_model_wrapper import ModelWrapper

from .subject_locator_wrapper_mixin import SubjectLocatorModelWrapperMixin



class SubjectScreeningModelWrapper(SubjectLocatorModelWrapperMixin, ModelWrapper):

    model = 'potlako_subject.subjectscreening'
    querystring_attrs = ['screening_identifier']
    next_url_attrs = ['screening_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get('screening_listboard_url')
