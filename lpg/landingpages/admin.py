from django.db import models
from django.contrib.auth.models import User, UserManager, Permission
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django import forms

from lpg.landingpages.models import *



def get_perm(Model, perm):
    '''
    Return the permission object, for the Model
    '''
    ct = ContentType.objects.get_for_model(Model)
    return Permission.objects.get(content_type=ct,codename=perm)

'''
Currency Admin
'''
class CurrencyAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'timestamp')
    
'''
Plan Admin
'''
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_of_pages', 'cost', 'timestamp')
    
'''
Account Admin
'''

class AccountAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Account Administration', {'fields' : ['name', 'currency']}),
    ]
    class Media:
        js = (
            '/media/js/jquery/jquery-1.3.2.min.js',
            '/media/js/lpg.js',
        )
    
    def save_model(self, request, obj, form, change):
        #user_id = request.REQUEST.get('user',None)
        #user = User.objects.get(id=user_id)

        #user_id = request.user_id
        obj.user_id = request.user.id
        user = User.objects.get(id=request.user.id)
        
        '''
        Remove Account Add permissions to establish a profile before save
        '''
        user.user_permissions.remove(get_perm(Account,
                                           Account._meta.get_add_permission()))

	'''
	Add Account Edit permissions
	'''
	#user.user_permissions.add(get_perm(Account,
	#				   Account._meta.get_change_permission()))

        '''
        Grant Landing Page Add/Edit/Delete permissions
        '''
        user.user_permissions.add(get_perm(LandingPage,
                                           LandingPage._meta.get_add_permission()))
        user.user_permissions.add(get_perm(LandingPage,
                                           LandingPage._meta.get_change_permission()))
        user.user_permissions.add(get_perm(LandingPage,
                                           LandingPage._meta.get_delete_permission()))
        '''
        Grant Domain Add/Edit/Delete permissions
        '''
        user.user_permissions.add(get_perm(Domain,
                                           Domain._meta.get_add_permission()))
        user.user_permissions.add(get_perm(Domain,
                                           Domain._meta.get_change_permission()))
        user.user_permissions.add(get_perm(Domain,
                                           Domain._meta.get_delete_permission()))
        obj.active = True
        
        
        user.save()
        obj.save()

    list_display = ( 'name', 'active', 'timestamp', )
    
'''
LandingPage Admin
'''
class LandingPageAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Select domain', {'fields' : ['domain_name']}),
        ('SEO Data', {'fields' : ['url', 'meta_description', 'meta_keywords', 'title'], 'classes' : ['wide']}),
        ('Layout', {'fields' : ['layout']}),
        ('Content', {'fields' : ['logo', 'heading', 'body'], 'classes' : ['collapse']}),
        ('Backgrounds', {'fields' : ['background_color', 'background_image', 'background_repeat'], 'classes' : ['collapse']}),
        ('Media', {'fields' : ['add_media', 'photo', 'embed_media'], 'classes' : ['collapse toggle_media']}),
        ('Forms', {'fields' : ['call_to_action_form', 'google_analytics_form'], 'classes' : ['collapse']}),
        ('Footer', {'fields' : ['footer'], 'classes' : ['collapse', 'wide']}),
        ('Public', {'fields' : ['draft']}),
    ]
    
    list_display = ( 'url', 'domain_name', 'timestamp' )
    
    class Media:
        js = (
            '/media/js/jquery/jquery-1.3.2.min.js',
            '/media/js/jquery.tinymce.js',
            '/media/js/tiny_mce/tiny_mce.js',
            '/media/js/jquery/plugins/jquery.dimensions.js',
            '/media/js/jquery/plugins/jquery.tooltip.js',
            '/media/js/jscolor/jscolor.js',
            '/media/js/lpg.js',
        )
        
        css = {
            'all' : ('/media/css/admin.css',)
        }

    def queryset(self, request):
        if request.user.is_superuser:
            return LandingPage.objects.all()
        else:
            return LandingPage.objects.filter(user_id=request.user.id)

    def get_form(self, request, obj=None):
        self.request = request
        f = super(LandingPageAdmin,self).get_form(request, obj)
        return f
    
    def formfield_for_dbfield(self, dbfield, **kwargs):
        if dbfield.name == 'domain_name':
            kwargs['queryset'] = Domain.objects.filter(user_id=self.request.user.id)
        return super(LandingPageAdmin, self).formfield_for_dbfield(dbfield, **kwargs)
    
    def save_model(self, request, obj, form, change):
        
        '''
        Remove permissions to add when you reach the Quota limit!
        '''
        user = User.objects.get(id=request.user.id)
        
        '''
        Get current number of Landing Pages owned by request.user
        '''
        lp = LandingPage.objects.filter(user_id=request.user.id)
        
        '''
        Number of Landing Pages + 1
        '''
        lp_count = lp.count() + 1

        account = Account.objects.filter(user=request.user.id)

        domain = Domain.objects.get(id=obj.domain_name_id)
        
        plan = Plan.objects.get(id=domain.plan_id)
        
        '''
        Number of Pages in plan (under Domain object)
        '''
        limit_count = plan.number_of_pages
            
        '''
        Remove LandingPage add permission if user reaches quota.
        '''
        if lp_count == limit_count:
            user.user_permissions.remove(get_perm(LandingPage,
                                           LandingPage._meta.get_add_permission()))
        user.save()
        
        obj.user_id = request.user.id
        obj.save()
     
    #def delete_model(self, request, obj):
        '''
        Add permissions to create LandingPage when you Delete
        '''

    #    user = User.objects.get(id=request.user.id)
    #    
    #    user.user_permissions.add(get_perm(LandingPage,
    #                                       LandingPage._meta.get_add_permission()))
    #    self.delete()
    #    
'''
Register Models
'''

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(LandingPage, LandingPageAdmin)
admin.site.register(Layout, LayoutAdmin)
