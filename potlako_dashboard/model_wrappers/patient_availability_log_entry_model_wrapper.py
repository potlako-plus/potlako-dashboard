from django.conf import settings

from edc_model_wrapper.wrappers import ModelWrapper


class PatientAvailabilityLogEntryModelWrapper(ModelWrapper):

    model = 'potlako_subject.patientavailabilitylogentry'
    next_url_name = settings.DASHBOARD_URL_NAMES.get(
                                'screening_listboard_url')
    querystring_attrs = ['patient_availability_log']
    next_url_attrs = ['screening_identifier']

    @property
    def screening_identifier(self):
        return self.object.patient_availability_log.clinician_call.screening_identifier

    @property
    def patient_availability_log(self):
        return self.object.patient_availability_log.id
