from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import TemplateRequestContextMixin
from edc_base.utils import get_utcnow
from edc_navbar import NavbarViewMixin
from django.contrib import messages

from .pdf_response_mixin import PdfResponseMixin
from ...model_wrappers import VerbalConsentModelWrapper, SubjectConsentModelWrapper
from potlako_subject.forms import VerbalConsentForm
from django.http.response import HttpResponseRedirect


class VerbalConsentView(PdfResponseMixin, NavbarViewMixin, EdcBaseViewMixin,
                        TemplateRequestContextMixin, TemplateView):

    template_name = 'procurement_dashboard/purchase_order/dashboard.html'
    report_template = 'verbal_consent_template'
    report_pdf_template = 'verbal_consent_template_pdf'
    model = 'potlako_subject.verbalconsent'
    pdf_name = 'verbal_consent'
    navbar_name = 'potlako_dashboard'
    navbar_selected_item = 'eligible_subjects'
    verbal_script_model_wrapper_cls = VerbalConsentModelWrapper
    form_class = VerbalConsentForm
    subject_consent_model_wrapper_cls = SubjectConsentModelWrapper

    @property
    def model_cls(self):
        return django_apps.get_model('potlako_subject.verbalconsent')

    @property
    def subject_consent_model_cls(self):
        return django_apps.get_model('potlako_subject.subjectconsent')

    def post(self, request, *args, **kwargs):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            self.upload_to = self.model_cls.file.field.upload_to
            # create a form instance and populate it with data from the request:


            # form = VerbalConsentForm(request.POST)
            context = self.get_context_data(**kwargs)

            options = {
                'screening_identifier': context.get('screening_identifier'),
                'user_uploaded': request.user.first_name + " " + self.request.user.last_name,
                'language': context.get('language'),
                'datetime_captured': get_utcnow(),
                'version': '1'}
            verbal_consent_model = self.model_cls(
                **options,
                user_created=request.user.username,
                created=get_utcnow())

            context.update(
                **options,
                participant_name=request.POST['participant_name'],
                designation=request.POST['designation'],
                signature=request.POST['signature'],
                consented=request.POST['consented'])


#             f_name, lname = request.POST['participant_name'].split(" ")

            self.handle_uploaded_file(context, model_obj=verbal_consent_model, **kwargs)

                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
            return self.view_pdf(context)

#                 return HttpResponseRedirect(
#                     self.add_consent_href(fname=f_name, lname=l_name))

    def add_consent_href(self, fname=None, lname=None):
        """Returns a wrapped saved or unsaved subject screening.
        """
        screening_identifier = self.kwargs.get('screening_identifier')
        model_obj = self.subject_consent_model_cls(
            screening_identifier=screening_identifier,
            first_name=fname,
            last_name=lname)
        return self.subject_consent_model_wrapper_cls(model_obj=model_obj).href

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        screening_identifier = self.kwargs.get('screening_identifier', None)

        context.update(
            verbal_consent_datetime=get_utcnow(),
            screening_identifier=screening_identifier,
            language=self.request.GET.get('language', 'en'),
            verbal_consent_href=self.model_cls().get_absolute_url(),
            add_consent_href=self.add_consent_href, )
        return context

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
    def pdf_template(self):
#         language=self.context.get('language', 'en')
#         return f'potlako_dashboard/screening/verbal_consent_{language}_pdf.html'
        return f'potlako_dashboard/screening/verbal_consent_pdf.html'
