from django.conf import settings
from edc_model_wrapper.wrappers import ModelWrapper


class SpecialFormsModelWrapper(ModelWrapper):

    next_url_name = settings.DASHBOARD_URL_NAMES.get('subject_dashboard_url')
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['symptoms_discussion', 'discussion_date', 'discussion_date_estimated',
                         'discussion_date_estimation', 'seek_help_date', 'seek_help_date_estimated', 'seek_help_date_estimation']
