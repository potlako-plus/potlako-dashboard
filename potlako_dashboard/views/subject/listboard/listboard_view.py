import re
from django.apps import apps as django_apps
from django.db.models import Q
from edc_base.view_mixins import EdcBaseViewMixin
from edc_dashboard.view_mixins import (
    ListboardFilterViewMixin, SearchFormViewMixin)
from edc_dashboard.views import ListboardView as BaseListBoardView
from edc_navbar import NavbarViewMixin

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

        navigation_cls = django_apps.get_model('potlako_subject.navigationsummaryandplan')
        navigation_identifiers = navigation_cls.objects.values_list('subject_identifier')
        intervention_identifiers = self.get_community_queryset('Intervention')

        queryset = super().get_queryset()
        self.request.GET.get('p_role')
        usr_groups = [g.name for g in self.request.user.groups.all()]
        if (any(map((lambda value: value in usr_groups), ['Supervisor', 'HR']))
                and self.request.GET.get('p_role') in ['Supervisor', 'HR']):
            queryset = queryset.filter(status__in=['approved', 'verified', 'submitted'])

        if self.request.GET.get('dept'):
            usr_groups = [g.name for g in self.request.user.groups.all()]

            if 'HR' in usr_groups and self.request.GET.get('p_role') == 'HR':
                queryset = queryset.filter(
                    employee__department__dept_name=self.request.GET.get('dept'))

        if self.request.GET.get('f') == 'navigation':
            queryset = queryset.filter(
                Q(subject_identifier__in=navigation_identifiers) & Q(
                    subject_identifier__in=intervention_identifiers))
        elif self.request.GET.get('f') == 'no_navigation':
            queryset = queryset.exclude(
                Q(subject_identifier__in=navigation_identifiers) & Q(
                    subject_identifier__in=intervention_identifiers))
        elif self.request.GET.get('f') == 'intervention':
            queryset = queryset.filter(subject_identifier__in=intervention_identifiers)
        elif self.request.GET.get('f') == 'soc':
            queryset = queryset.exclude(
                Q(subject_identifier__in=navigation_identifiers) | Q(
                    subject_identifier__in=intervention_identifiers))
        return queryset

    def get_queryset_filter_options(self, request, *args, **kwargs):
        """Returns filter options applied to every
        queryset.
        """
        return {}

    def get_community_queryset(self, community_name):
        onschedule_cls = django_apps.get_model('potlako_subject.onschedule')
        return onschedule_cls.objects.filter(community_arm=community_name).values_list('subject_identifier')

    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q
