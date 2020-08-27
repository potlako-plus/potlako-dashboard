from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('potlako_dashboard/buttons/screening_button.html')
def screening_button(model_wrapper):
    return dict(
        add_screening_href=model_wrapper.subject_screening.href,
        screening_identifier=model_wrapper.object.screening_identifier,
        subject_screening_obj=model_wrapper.subject_screening_model_obj)


@register.inclusion_tag('potlako_dashboard/buttons/clinician_call_enrollment_button.html')
def clinician_call_enrollment_button(model_wrapper):
    title = ['Edit Clinician Call Enrollment form.']
    return dict(
        screening_identifier=model_wrapper.object.screening_identifier,
        href=model_wrapper.href,
        title=' '.join(title))


@register.inclusion_tag('potlako_dashboard/buttons/eligibility_button.html')
def eligibility_button(model_wrapper):
    comment = []
    obj = model_wrapper.subject_screening_model_obj or model_wrapper.object
    tooltip = None
    if not obj.is_eligible and obj.ineligibility:
        comment = obj.ineligibility.strip('[').strip(']').split(',')
    comment = list(set(comment))
    comment.sort()
    return dict(is_eligible=obj.is_eligible, comment=comment, tooltip=tooltip)


@register.inclusion_tag('potlako_dashboard/buttons/subject_locator_button.html')
def subject_locator_button(model_wrapper):
    title = ['Add subject Locator.']
    return dict(
        subject_identifier=model_wrapper.subject_identifier,
        add_subject_locator_href=model_wrapper.subject_locator.href,
        subject_locator_model_obj=model_wrapper.subject_locator_model_obj,
        title=' '.join(title))
    
@register.inclusion_tag('potlako_dashboard/buttons/baseline_clinical_summary_button.html')
def baseline_clinical_summary_button(model_wrapper):
    title = ['Add baseline clinical summary.']
    return dict(
        subject_identifier=model_wrapper.subject_identifier,
        add_baseline_summary_href=model_wrapper.baseline_summary.href,
        baseline_summary_model_obj=model_wrapper.baseline_summary_model_obj,
        title=' '.join(title))


@register.inclusion_tag('potlako_dashboard/buttons/consent_button.html')
def consent_button(model_wrapper):
    title = ['Consent subject to participate.']
    return dict(
        screening_identifier=model_wrapper.object.screening_identifier,
        subject_identifier=model_wrapper.subject_identifier,
        subject_screening_obj=model_wrapper.subject_screening_model_obj,
        add_consent_href=model_wrapper.consent.href,
        consent_version=model_wrapper.consent_version,
        title=' '.join(title))


@register.inclusion_tag('potlako_dashboard/buttons/dashboard_button.html')
def dashboard_button(model_wrapper):
    subject_dashboard_url = settings.DASHBOARD_URL_NAMES.get(
        'subject_dashboard_url')
    return dict(
        subject_dashboard_url=subject_dashboard_url,
        subject_identifier=model_wrapper.subject_identifier)
