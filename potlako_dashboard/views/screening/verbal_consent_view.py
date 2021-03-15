from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import TemplateRequestContextMixin
from edc_base.utils import get_utcnow
from edc_navbar import NavbarViewMixin

from .pdf_response_mixin import PdfResponseMixin
from ...model_wrappers import SubjectConsentModelWrapper
from potlako_subject.forms import VerbalConsentForm
from django.http.response import HttpResponseRedirect


class VerbalConsentView(PdfResponseMixin, NavbarViewMixin, EdcBaseViewMixin,
                        TemplateRequestContextMixin, TemplateView):

    report_template = 'verbal_consent_template'
    report_pdf_template = 'verbal_consent_template_pdf'
    model = 'potlako_subject.verbalconsent'
    navbar_name = 'potlako_dashboard'
    navbar_selected_item = 'eligible_subjects'
    form_class = VerbalConsentForm
    subject_consent_model_wrapper_cls = SubjectConsentModelWrapper

    @property
    def pdf_name(self):
        screening_identifier = self.kwargs.get('screening_identifier')
        last_name = self.clinician_call_field_value(screening_identifier, 'last_name')
        return f'{last_name}{screening_identifier}'

    @property
    def model_cls(self):
        return django_apps.get_model('potlako_subject.verbalconsent')

    @property
    def subject_consent_model_cls(self):
        return django_apps.get_model('potlako_subject.subjectconsent')

    @property
    def clinician_call_model_cls(self):
        return django_apps.get_model('potlako_subject.cliniciancallenrollment')

    def post(self, request, *args, **kwargs):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            self.upload_to = self.model_cls.file.field.upload_to
            # create a form instance and populate it with data from the request:

            context = self.get_context_data(**kwargs)

            options = {
                'screening_identifier': context.get('screening_identifier'),
                'user_uploaded': request.user.first_name + " " + self.request.user.last_name,
                'language': request.POST['language'],
                'consented': request.POST['consented'],
                'datetime_captured': get_utcnow(),
                'version': '1',
                'designation': request.POST['designation'],
                'signature': request.POST['signature']}

#             verbal_consent_form = self.form_class(options)
            if self.verbal_consent_obj:
                verbal_consent_obj = self.verbal_consent_obj
                if verbal_consent_obj.consented != request.POST['consented']:
                    verbal_consent_obj.user_uploaded = options.get('user_uploaded')
                    verbal_consent_obj.consented = options.get('consented')
                    verbal_consent_obj.datetime_captured
                    verbal_consent_obj.save()
                    verbal_consent_model = self.verbal_consent_obj
                else:
                    return HttpResponseRedirect(reverse('potlako_dashboard:screening_listboard_url',
                                                kwargs=dict(screening_identifier=self.kwargs.get('screening_identifier'),)))
            else:
                verbal_consent_model = self.model_cls(
                    **options,
                    user_created=request.user.username,
                    created=get_utcnow())
                context.update(
                    **options,
                    participant_name=request.POST['participant_name'],)
            f_name, l_name = request.POST['participant_name'].split(" ")
            language = request.POST['language']

            self.handle_uploaded_file(context, model_obj=verbal_consent_model, **kwargs)
            if request.POST['consented'] == 'Yes':
                return HttpResponseRedirect(
                    self.add_consent_href(fname=f_name, lname=l_name, language=language))
            return HttpResponseRedirect(reverse('potlako_dashboard:screening_listboard_url',
                                        kwargs=dict(screening_identifier=self.kwargs.get('screening_identifier'),)))

    def add_consent_href(self, fname=None, lname=None, language=None):
        """Returns a wrapped saved or unsaved subject screening.
        """
        screening_identifier = self.kwargs.get('screening_identifier')
        model_obj = self.subject_consent_model_cls(
            screening_identifier=screening_identifier,
            first_name=fname,
            last_name=lname,
            language=language)
        return self.subject_consent_model_wrapper_cls(model_obj=model_obj).href

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        screening_identifier = self.kwargs.get('screening_identifier', None)
        f_name = self.clinician_call_field_value(screening_identifier, 'first_name')
        l_name = self.clinician_call_field_value(screening_identifier, 'last_name')
        full_name = f'{f_name} {l_name}'
        initials = None
        if self.verbal_consent_obj:
            initials = self.get_intiails(full_name=self.verbal_consent_obj.user_uploaded)

        context.update(
            verbal_consent_datetime=get_utcnow(),
            screening_identifier=screening_identifier,
            language=self.request.GET.get('language'),
            national_identity=self.clinician_call_field_value(
                screening_identifier, 'national_identity'),
            full_name=full_name,
            user_uploaded_initials=initials,
            verbal_consent_obj=self.verbal_consent_obj,
            add_consent_href=self.add_consent_href,)
        return context

    def get_intiails(self, full_name=None):
        if full_name:
            first_name, last_name = full_name.split(' ')
            return first_name.upper()[0] + last_name.upper()[0]
        return None

    def filter_options(self, **kwargs):
        options = super().filter_options(**kwargs)
        if self.kwargs.get('screening_identifier'):
            options.update(
                {'screening_identifier': kwargs.get('screening_identifier')})
        return options

    def get_template_names(self):
        language = self.request.GET.get('language', 'en')

        return f'potlako_dashboard/screening/verbal_consent_{language}.html'

    @property
    def verbal_consent_obj(self):
        try:
            return self.model_cls.objects.get(screening_identifier=self.kwargs.get('screening_identifier'))
        except self.model_cls.DoesNotExist:
            return None

    @property
    def pdf_template(self):
        language = self.request.POST['language']
        return f'potlako_dashboard/screening/verbal_consent_{language}_pdf.html'

    def clinician_call_field_value(self, screening_identifier, field_name):
        try:
            model_obj = self.clinician_call_model_cls.objects.get(
                screening_identifier=screening_identifier)
        except self.clinician_call_model_cls.DoesNotExist:
            raise ValidationError(
                'Clinician Call Enrollment object does not exist.')
        else:
            return getattr(model_obj, field_name)
