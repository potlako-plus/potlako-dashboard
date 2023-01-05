
from django.apps import apps as django_apps

class NavigationHistoryMixin:
    
    navigation_plan_model = 'potlako_subject.navigationsummaryandplan'
    
    
    
    @property
    def navigation_plan_cls(self):
        return django_apps.get_model(self.navigation_plan_model)
    
    @property
    def navigation_plan_history_objs(self):
        subject_identifier = self.consent.subject_identifier
    
        objs = self.navigation_plan_cls.history.filter(subject_identifier = subject_identifier)[:10]
        
        return objs
    
    @property
    def navigation_plan_inlines(self):
        
        inlines = [];
        
        for plan in self.navigation_plan_history_objs:
            
            inlines.append(list(plan.evaluationtimeline_set.all()))
            
        return inlines