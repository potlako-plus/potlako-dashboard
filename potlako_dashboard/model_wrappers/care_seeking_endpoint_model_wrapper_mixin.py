from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from .special_forms_model_wrapper import SpecialFormsModelWrapper


class CareSeekingEndpointModelWrapperMixin:

    care_seeking_endpoint_model_wrapper_cls = SpecialFormsModelWrapper

    @property
    def care_seeking_endpoint_model_obj(self):
        """Returns a symptoms and care seeking endpoint model
        instance or None.
        """
        try:
            return self.care_seeking_endpoint_cls.objects.get(
                **self.care_seeking_endpoint_options)
        except ObjectDoesNotExist:
            return None

    @property
    def care_seeking_endpoint(self):
        """Returns a wrapped saved or unsaved symptom and care seeking recording .
        """
        model_obj = self.care_seeking_endpoint_model_obj or self.care_seeking_endpoint_cls(
            **self.create_care_seeking_endpoint_options)
        return self.care_seeking_endpoint_model_wrapper_cls(model_obj=model_obj)

    @property
    def symptom_cx_assessment_cls(self):
        return django_apps.get_model('potlako_subject.symptomandcareseekingassessment')

    @property
    def symptom_cx_assessment_model_obj(self):
        """Returns a symptoms assessment object fields
        """
        try:
            return self.symptom_cx_assessment_cls.objects.get(subject_visit__subject_identifier=self.subject_identifier,
                                                              subject_visit__visit_code=1000)
        except ObjectDoesNotExist:
            return None

    @property
    def care_seeking_endpoint_cls(self):
        return django_apps.get_model('potlako_subject.symptomsandcareseekingendpoint')

    @property
    def create_care_seeking_endpoint_options(self):
        """Returns a dictionary of options to create a new
        unpersisted symptom and care seeking endpoint model instance.
        """

        options = dict(
            subject_identifier=self.subject_identifier,
            symptoms_discussion=self.symptom_cx_assessment_model_obj.symptoms_discussion,
            discussion_date=self.symptom_cx_assessment_model_obj.discussion_date.strftime("%d-%m-%Y") \
            if self.symptom_cx_assessment_model_obj.discussion_date else None,
            discussion_date_estimated=self.symptom_cx_assessment_model_obj.discussion_date_estimated,
            discussion_date_estimation=self.symptom_cx_assessment_model_obj.discussion_date_estimation,
            seek_help_date=self.symptom_cx_assessment_model_obj.clinic_visit_date.strftime("%d-%m-%Y") \
            if self.symptom_cx_assessment_model_obj.clinic_visit_date else None,
            seek_help_date_estimated=self.symptom_cx_assessment_model_obj.clinic_visit_date_estimated,
            seek_help_date_estimation=self.symptom_cx_assessment_model_obj.clinic_visit_date_estimation
            )
        return options

    @property
    def care_seeking_endpoint_options(self):
        """Returns a dictionary of options to get an existing
        symptom and care seeking endpoint instance.
        """
        options = dict(
            subject_identifier=self.subject_identifier)
        return options
