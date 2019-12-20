from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist

from edc_subject_dashboard import (
    AppointmentModelWrapper as BaseAppointmentModelWrapper)


class AppointmentModelWrapper(BaseAppointmentModelWrapper):
    pass
#     visit_model_wrapper_cls = SubjectVisitModelWrapper

#     @property
#     def wrapped_visit(self):
#         """Returns a wrapped persistent or non-persistent visit instance.
#         """
#         try:
#             model_obj = self.object.subjectvisit
#         except ObjectDoesNotExist:
#             visit_model = django_apps.get_model(
#                 self.visit_model_wrapper_cls.model)
#             model_obj = visit_model(
#                 appointment=self.object,
#                 subject_identifier=self.subject_identifier,
#                 reason=self.object.appt_reason)
#         return self.visit_model_wrapper_cls(model_obj=model_obj)
