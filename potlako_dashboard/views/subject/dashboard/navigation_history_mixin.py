
from django.apps import apps as django_apps

class NavigationHistoryMixin:
    
    navigation_plan_model = 'potlako_subject.navigationsummaryandplan'
    
    evaluation_timeline_model = 'potlako_subject.evaluationtimeline'
    
    
    
    @property
    def navigation_plan_cls(self):
        return django_apps.get_model(self.navigation_plan_model)
    
    @property
    def evaluation_timeline_cls(self):
        return django_apps.get_model(self.evaluation_timeline_model)
    
    @property
    def navigation_plan_history_objs(self):
        subject_identifier = self.consent.subject_identifier
    
        objs = self.navigation_plan_cls.history.filter(subject_identifier = subject_identifier)
        
        return objs
    
    @property
    def navigation_plan_history_objs(self):
        subject_identifier = self.consent.subject_identifier
    
        objs = self.navigation_plan_cls.history.filter(
            subject_identifier = subject_identifier).order_by('modified')
        
        return objs
    
    @property
    def current_navigation_plan(self):
        
        subject_identifier = self.consent.subject_identifier
    
        plan = self.navigation_plan_cls.objects.filter(subject_identifier = subject_identifier).first()
        
        return plan
    
    @property
    def current_navigation_plan_inlines(self):
        return self.current_navigation_plan.evaluationtimeline_set.all()
    
    @property
    def navigation_plan_inlines(self):
        
        subject_identifier = self.consent.subject_identifier
    
        objs = self.evaluation_timeline_cls.history.filter(
            navigation_plan__subject_identifier = subject_identifier)
        
        return objs