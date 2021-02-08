from django.conf import settings

from edc_model_wrapper.wrappers import ModelWrapper


class PatientAvailabilityLogModelWrapper(ModelWrapper):

    model = 'potlako_subject.patientavailabilitylog'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
        'screening_listboard_url')
    querystring_attrs = [
        'clinician_call', 'screening_identifier']
    next_url_attrs =[
        'clinician_call', 'screening_identifier']

    @property
    def screening_identifier(self):
        return self.object.clinician_call.screening_identifier

    @property
    def clinician_call(self):
        return self.object.clinician_call.id
