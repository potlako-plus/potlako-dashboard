import re

from django.apps import apps as django_apps
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls.base import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from edc_base.utils import get_utcnow
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import (
    ListboardFilterViewMixin, SearchFormViewMixin)
from edc_dashboard.views import ListboardView
from edc_navbar import NavbarViewMixin

from ....model_wrappers import SubjectConsentModelWrapper
from .filters import ListboardViewFilters
from .worklist_queryset_view_mixin import WorkListQuerysetViewMixin


class ListboardView(NavbarViewMixin, EdcBaseViewMixin,
                    ListboardFilterViewMixin, SearchFormViewMixin,
                    WorkListQuerysetViewMixin, ListboardView):

    listboard_template = 'potlako_worklist_template'
    listboard_url = 'potlako_worklist_url'
    listboard_panel_style = 'info'
    listboard_fa_icon = "fa-user-plus"

    model = 'potlako_subject.subjectconsent'
    listboard_view_filters = ListboardViewFilters()
    model_wrapper_cls = SubjectConsentModelWrapper
    navbar_name = 'potlako_dashboard'
    navbar_selected_item = 'worklist'
    ordering = '-modified'
    paginate_by = 10
    search_form_url = 'potlako_worklist_url'

    def get_success_url(self):
        return reverse('potlako_dashboard:potlako_worklist_url')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
#         context.update(
#             total_results=self.get_queryset().count(),)
        return context

    def get_queryset_filter_options(self, request, *args, **kwargs):
        options = super().get_queryset_filter_options(request, *args, **kwargs)
#         options.update(
#                 {'user_created': request.user.username})
        if kwargs.get('subject_identifier'):
            options.update(
                {'subject_identifier': kwargs.get('subject_identifier')})
        return options

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q
