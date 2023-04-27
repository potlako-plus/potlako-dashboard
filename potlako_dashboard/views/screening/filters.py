from edc_dashboard.listboard_filter import ListboardFilter, ListboardViewFilters


class ListboardViewFilters(ListboardViewFilters):

    all = ListboardFilter(
        name='all',
        label='All',
        lookup={})

    eligible = ListboardFilter(
        label='Eligible',
        position=10,
        lookup={'is_eligible': True})

    not_eligible = ListboardFilter(
        label='Not Eligible',
        position=11,
        lookup={'is_eligible': False})

    intervention = ListboardFilter(
        label='Intervention Community',
        position=12,
        )

    enhanced_care = ListboardFilter(
        label='Standard of Care Community',
        position=13,
        )
