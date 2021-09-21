from django.conf import settings

from edc_model_wrapper import ModelWrapper


class CoordinatorExitModelWrapper(ModelWrapper):

    model = 'potlako_prn.coordinatorexit'
    next_url_name = settings.DASHBOARD_URL_NAMES.get('subject_dashboard_url')
    next_url_attrs = ['subject_identifier']
    querystring_attrs = ['subject_identifier']
