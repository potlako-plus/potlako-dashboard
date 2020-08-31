import re
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView as BaseListboardView
from edc_navbar import NavbarViewMixin

from ...model_wrappers import SpecialFormsModelWrapper
from .filters import ListboardViewFilters


class ListBoardView(BaseListboardView, NavbarViewMixin, EdcBaseViewMixin,
                    ListboardFilterViewMixin, SearchFormViewMixin):

    listboard_template = 'endpoint_listboard_template'
    listboard_url = 'endpoint_listboard_url'
    listboard_panel_style = 'info'
    listboard_fa_icon = "fa-user-plus"

    listboard_view_filters = ListboardViewFilters()
    model = 'potlako_subject.cancerdiagnosisandtreatmentendpoint'
    model_wrapper_cls = SpecialFormsModelWrapper
    navbar_name = 'potlako_dashboard'
    navbar_selected_item = 'endpoint_recordings'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'endpoint_listboard_url'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    

    def get_context_data(self, **kwargs):
        print()
        context = super().get_context_data(**kwargs)
        context.update(
            cancer_diagnoses_and_treatment_add_url=self.model_cls().get_absolute_url())
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('subject_identifier'):
            options.update(
                {'subject_identifier': kwargs.get('subject_identifier')})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q
