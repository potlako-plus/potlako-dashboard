
from django.apps import apps as django_apps
from django.db.models import Q
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
    
        objs = self.navigation_plan_cls.history.filter(
            Q(subject_identifier = subject_identifier) & ~Q(user_created='potlako')).order_by('modified')
        
        return objs
    
    @property
    def current_navigation_plan(self):
        
        subject_identifier = self.consent.subject_identifier
        
        try:
            plan = self.navigation_plan_cls.objects.get(subject_identifier = subject_identifier)
        except self.navigation_plan_cls.DoesNotExist:
            pass
        else:
            return plan
    
    @property
    def current_navigation_plan_inlines(self):
        if self.current_navigation_plan:
            return self.current_navigation_plan.evaluationtimeline_set.order_by('created', 'modified')
        
    
    @property
    def evaluation_timelines_history_objs(self):
        inline = []
        
        if self.current_navigation_plan_inlines:
            
            for obj in self.current_navigation_plan_inlines:
                inline.append(obj.history.order_by('created','modified'))

        return inline
        
    @property
    def navigation_plan_inlines(self):
        
        subject_identifier = self.consent.subject_identifier
    
        objs = self.evaluation_timeline_cls.history.filter(
            navigation_plan__subject_identifier = subject_identifier)
        
        return objs