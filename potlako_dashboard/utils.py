from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist
from edc_base import get_utcnow
from edc_constants.constants import CANCELLED, CLOSED, NOT_DONE

action_item_model = 'edc_action_item.actionitem'

action_item_model_cls = django_apps.get_model(action_item_model)


def open_action_items(subject_identifier):
    return action_item_model_cls.objects.filter(
        subject_identifier=subject_identifier,
        action_type__show_on_dashboard=True).exclude(
        status__in=[CLOSED, CANCELLED]).order_by('-report_datetime')


def community_arm(subject_identifier):
    onschedule_model_cls = django_apps.get_model(
        'potlako_subject.onschedule')
    try:
        onschedule_obj = onschedule_model_cls.objects.get(
            subject_identifier=subject_identifier)
    except ObjectDoesNotExist:
        return None
    else:
        return onschedule_obj.community_arm


def determine_flag(subject_identifier):
    keysteps_form = django_apps.get_model(
        'potlako_subject.evaluationtimeline')

    key_steps = keysteps_form.objects.filter(
        navigation_plan__subject_identifier=subject_identifier,
        key_step_status=NOT_DONE)
    flags = []

    for key_step in key_steps:
        today = get_utcnow().date()
        target_date = key_step.target_date

        if (today - target_date).days > 7:
            flags.append('past')
        elif (target_date - today).days > 7:
            flags.append('early')
        else:
            flags.append('on_time')

    next((flags.append('past') for obj in open_action_items(subject_identifier) if
          'Standard' in community_arm(subject_identifier) and 'navigationsummaryandplan'
          in obj.reference_model), None)

    flags = list(set(flags))
    return max(flags) if flags else 'default'
