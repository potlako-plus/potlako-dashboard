from edc_dashboard.listboard_filter import ListboardFilter, ListboardViewFilters


class ListboardViewFilters(ListboardViewFilters):

    all = ListboardFilter(
        name='all',
        label='All',
        lookup={})

    navigation = ListboardFilter(
        label='With Navigation Plan',
        position=10,
        lookup={'navigation': True})

    no_navigation = ListboardFilter(
        label='Without Navigation Plan',
        position=11,
        lookup={'no_navigation': True})

    intervention = ListboardFilter(
        label='Intervention Community',
        position=12,
        lookup={'community_arm': 'Intervention'})

    soc = ListboardFilter(
        label='Standard of Care Community',
        position=13,
        lookup={'community_arm': 'Standard of Care'})
