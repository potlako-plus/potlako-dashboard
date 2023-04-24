import re

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
import ast

from edc_dashboard.view_mixins import ListboardFilterViewMixin, SearchFormViewMixin
from edc_dashboard.views import ListboardView

from ...model_wrappers import ClinicianCallEnrollmentModelWrapper
from .filters import ListboardViewFilters


class ListBoardView(NavbarViewMixin, EdcBaseViewMixin,
                    ListboardFilterViewMixin, SearchFormViewMixin, ListboardView):
    listboard_template = 'screening_listboard_template'
    listboard_url = 'screening_listboard_url'
    listboard_panel_style = 'info'
    listboard_fa_icon = "fa-user-plus"

    listboard_view_filters = ListboardViewFilters()
    model = 'potlako_subject.cliniciancallenrollment'
    model_wrapper_cls = ClinicianCallEnrollmentModelWrapper
    navbar_name = 'potlako_dashboard'
    navbar_selected_item = 'eligible_subject'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'screening_listboard_url'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            clinician_call_enrollment_add_url=self.model_cls().get_absolute_url(),
        )
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
        if kwargs.get('screening_identifier'):
            options.update(
                {'screening_identifier': kwargs.get('screening_identifier')},)
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Za-z]+$', search_term):
            q = Q(user_created__icontains=search_term) | Q(facility__icontains=search_term)
        return q

    def get_queryset(self):
        communities = settings.COMMUNITIES
        facility_filter = self.request.GET.get('f')

        if facility_filter in ['intervention', 'enhanced_care']:
            community_list = ast.literal_eval(communities.get(facility_filter))
            queryset = super().get_queryset().filter(facility__in=community_list)
        else:
            queryset = super().get_queryset()

        return queryset
