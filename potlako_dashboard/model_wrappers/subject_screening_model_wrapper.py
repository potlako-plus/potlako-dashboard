from django.conf import settings
from edc_model_wrapper import ModelWrapper

from .subject_locator_model_wrapper_mixin import (
    SubjectLocatorModelWrapperMixin)
from .baseline_summary_model_wrapper_mixin import BaselineClinicalSummaryModelWrapperMixin


class SubjectScreeningModelWrapper(
        SubjectLocatorModelWrapperMixin,
        BaselineClinicalSummaryModelWrapperMixin, ModelWrapper):

    model = 'potlako_subject.subjectscreening'
    querystring_attrs = ['screening_identifier']
    next_url_attrs = ['screening_identifier']
    next_url_name = settings.DASHBOARD_URL_NAMES.get('screening_listboard_url')
