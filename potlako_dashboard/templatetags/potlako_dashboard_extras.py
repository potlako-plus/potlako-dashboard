from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('potlako_dashboard/buttons/screening_button.html')
def screening_button(model_wrapper):
    title = ['Edit subject\' screening form.']
    return dict(
        screening_identifier=model_wrapper.object.screening_identifier,
        href=model_wrapper.href,
        title=' '.join(title))


@register.inclusion_tag('potlako_dashboard/buttons/eligibility_button.html')
def eligibility_button(subject_screening_model_wrapper):
    comment = []
    obj = subject_screening_model_wrapper.object
    tooltip = None
    if not obj.eligible:
        comment = obj.reasons_ineligible.split(',')
    comment = list(set(comment))
    comment.sort()
    return dict(eligible=obj.eligible, comment=comment, tooltip=tooltip)


@register.inclusion_tag('potlako_dashboard/buttons/consent_button.html')
def consent_button(model_wrapper):
    title = ['Consent subject to participate.']
    consent_version = model_wrapper.consent.version
    return dict(
        screening_identifier=model_wrapper.object.screening_identifier,
        subject_identifier=model_wrapper.object.subject_identifier,
        add_consent_href=model_wrapper.consent.href,
        consent_version=consent_version,
        title=' '.join(title))


@register.inclusion_tag('potlako_dashboard/buttons/dashboard_button.html')
def dashboard_button(model_wrapper):
    subject_dashboard_url = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')
    return dict(
        subject_dashboard_url=subject_dashboard_url,
        subject_identifier=model_wrapper.subject_identifier)
