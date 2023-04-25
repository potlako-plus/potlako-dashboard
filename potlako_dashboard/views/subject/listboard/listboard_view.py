import re

from django.apps import apps as django_apps
from django.db.models import Q
from django.utils.html import escape
from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin

from edc_dashboard.view_mixins import (
    ListboardFilterViewMixin, SearchFormViewMixin)
from edc_dashboard.views import ListboardView as BaseListBoardView
from potlako_dashboard.model_wrappers import SubjectConsentModelWrapper

from .filters import ListboardViewFilters


class ListboardView(EdcBaseViewMixin, NavbarViewMixin,
                    ListboardFilterViewMixin, SearchFormViewMixin,
                    BaseListBoardView):

    listboard_template = 'subject_listboard_template'
    listboard_url = 'subject_listboard_url'
    listboard_panel_style = 'success'
    listboard_fa_icon = "far fa-user-circle"
    model = 'potlako_subject.subjectconsent'
    model_wrapper_cls = SubjectConsentModelWrapper
    app_config_name = 'potlako_dashboard'
    navbar_name = 'potlako_dashboard'
    navbar_selected_item = 'consented_subject'
    search_form_url = 'subject_listboard_url'
    listboard_view_filters = ListboardViewFilters()

    def get_queryset(self):
        ''' Method to filter queryset by a filter or community search, returns a wrapped
         queryset because of the community search which is a model wrapper property.'''

        navigation_cls = django_apps.get_model('potlako_subject.navigationsummaryandplan')
        navigation_identifiers = navigation_cls.objects.values_list('subject_identifier')
        intervention_identifiers = self.get_community_queryset('Intervention')

        queryset = super().get_queryset()

        to_order = True

        if self.request.GET.get('f') == 'navigation':
            queryset = queryset.filter(
                Q(subject_identifier__in=navigation_identifiers) & Q(
                    subject_identifier__in=intervention_identifiers))
        elif self.request.GET.get('f') == 'no_navigation':
            queryset = queryset.filter(
                    subject_identifier__in=intervention_identifiers).exclude(
                        subject_identifier__in=navigation_identifiers)
        elif self.request.GET.get('f') == 'intervention':
            queryset = queryset.filter(subject_identifier__in=intervention_identifiers)
        elif self.request.GET.get('f') == 'soc':
            queryset = queryset.exclude(
                Q(subject_identifier__in=navigation_identifiers) | Q(
                    subject_identifier__in=intervention_identifiers))

            to_order = False

        search_term = self.request.GET.get('q')

        if search_term and search_term.startswith('c:'):
            queryset = self.get_ordered_queryset(queryset, to_order, search_term)

        else:
            queryset = self.get_ordered_queryset(queryset, to_order)

        return queryset

    def get_ordered_queryset(self, queryset, to_order=False, search_term=None):
        ''' Order queryset according to navigation status, includes optional argument to
         filter by a particular search term.'''

        ordering = ['past', 'on_time', 'early', 'default']

        wrapped_qs = []

        for obj in queryset:
            wrapped_qs.append(self.model_wrapper_cls(obj))

        if search_term and search_term.startswith('c:'):
            search_term_filtered = search_term[2:].lower()
            filtered_wrapped_qs = [item for item in wrapped_qs if
                                   search_term_filtered in item.subject_community.lower()]
            return filtered_wrapped_qs

        ordered_qs = []

        if to_order:
            for order in ordering:
                ordered_qs += [item for item in wrapped_qs if
                               item.navigation_status == order]

        return ordered_qs or wrapped_qs

    def get_wrapped_queryset(self, queryset):
        return queryset

    def get_queryset_filter_options(self, request, *args, **kwargs):
        """Returns filter options applied to every queryset.
        """
        return {}

    def get_community_queryset(self, community_name):
        onschedule_cls = django_apps.get_model('potlako_subject.onschedule')
        return onschedule_cls.objects.filter(
            community_arm=community_name).values_list('subject_identifier')

    @property
    def search_term(self):
        if not self._search_term:
            search_term = self.request.GET.get('q')
            if search_term and search_term[:2] != 'c:':
                if search_term:
                    search_term = escape(search_term).strip()
                search_term = self.clean_search_term(search_term)
                self._search_term = search_term
            else:
                self._search_term = None
        return self._search_term

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Za-z]+$', search_term):
            q = Q(user_created__icontains=search_term)
        return q
