from django.conf import settings
from edc_model_wrapper.wrappers import ModelWrapper


class SpecialFormsModelWrapper(ModelWrapper):

    next_url_name = settings.DASHBOARD_URL_NAMES.get('subject_dashboard_url')
    next_url_attrs = ['subject_identifier']
