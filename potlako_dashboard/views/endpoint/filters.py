from edc_constants.constants import OTHER
from edc_dashboard.listboard_filter import ListboardFilter, ListboardViewFilters


class ListboardViewFilters(ListboardViewFilters):

    all = ListboardFilter(
        name='all',
        label='All',
        lookup={})

    # Cancer Evaluation
    complete = ListboardFilter(
        label='Cancer Evaluation Complete',
        position=10,
        lookup={'cancerdxandtxendpoint.cancer_evaluation': 'complete'})

    unable_to_complete = ListboardFilter(
        label='Cancer Evaluation Incomplete',
        position=11,
        lookup={'cancerdxandtxendpoint.cancer_evaluation':
                'unable_to_complete'})

    incomplete_ongoing_evaluation = ListboardFilter(
        label='Incomplete, ongoing evaluation',
        position=12,
        lookup={'cancerdxandtxendpoint.cancer_evaluation':
                'incomplete_ongoing_evaluation'})

    incomplete_12_months = ListboardFilter(
        label='Incomplete, 12 month visit',
        position=13,
        lookup={'cancerdxandtxendpoint.cancer_evaluation':
                'incomplete_12_months'})

    final_cancer_diagnosis = ListboardFilter(
        label='Final Cancer Diagnosis',
        position=14,
        lookup={'cancerdxandtxendpoint.final_cancer_diagnosis__isnull':
                False})

    non_cancer_diagnosis = ListboardFilter(
        label='Final Non-Cancer diagnosis',
        position=15,
        lookup={'cancerdxandtxendpoint.non_cancer_diagnosis__isnull':
                False})
