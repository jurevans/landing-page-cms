from django.db import models
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django import forms

'''
    Landing page model definitions
'''

class Layout(models.Model):
    name = models.CharField(max_length=20)
    template = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name
    
class LayoutAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'template', 'timestamp' )

BACKGROUND_CHOICES = (
    ('N', 'Set as Background Image'),
    ('R', 'Tile'),
    ('X', 'Repeat Horizontally'),
)

class LandingPage(models.Model):
    editor = models.ForeignKey(User, help_text='Put help-text here!')
    url = models.SlugField(max_length=50, unique=True, help_text='Put help-text here!')
    title = models.CharField(max_length=80, null=True, blank=True, help_text='Put help-text here!')
    heading = models.CharField(max_length=80, help_text='Put help-text here!')
    body = models.TextField(help_text='Put help-text here!')
    body_image = models.ImageField(upload_to='uploads/images', null=True, blank=True, help_text='Put help-text here!')
    embed_media = models.CharField(max_length=250, null=True, blank=True, help_text='Put help-text here!')
    layout = models.ForeignKey(Layout, help_text='Put help-text here!')
    logo = models.ImageField(upload_to='uploads/logos', help_text='Put help-text here!')
    background_color = models.CharField(max_length=7, null=True, blank=True, help_text='Put help-text here!')
    background_image = models.ImageField(upload_to='uploads/backgrounds', null=True, blank=True, help_text='Put help-text here!')
    background_repeat = models.CharField(max_length=1, choices=BACKGROUND_CHOICES, null=True, blank=True, help_text='Put help-text here!')
    meta_description = models.CharField(max_length=250, null=True, blank=True, help_text='Put help-text here!')
    meta_keywords = models.CharField(max_length=250, null=True, blank=True, help_text='Put help-text here!')
    call_to_action_form = models.TextField(null=True, blank=True, help_text='Put help-text here!')
    google_analytics_form = models.TextField(null=True, blank=True, help_text='Put help-text here!')
    footer = models.CharField(max_length=250, help_text='Put help-text here!')
    timestamp = models.DateTimeField(auto_now=True, help_text='Put help-text here!')
    
    def __unicode__(self):
        return self.url

class LandingPageForm(forms.ModelForm):
    background_color = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class' : 'color'})
    )
    
    body = forms.CharField(
        widget=forms.Textarea(attrs={'class' : 'tinymce'})
    )
    
    # How to do this?
    #layout = forms.ForeignKey(
    #    widget=forms.RadioSelect()
    #)
    
    call_to_action_form = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class' : 'no_tinymce'})
    )
    
    google_analytics_form = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class' : 'no_tinymce'})
    )
    
    class Meta:
        model = LandingPage
        #exclude = ['editor',] # Need better way to do this!

#class LandingPageAdminForm(forms.ModelForm):
    

class LandingPageAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Select editor', {'fields' : ['editor']}),
        ('SEO Data', {'fields' : ['url', 'meta_description', 'meta_keywords', 'title'], 'classes' : ['wide']}),
        ('Layout', {'fields' : ['layout']}),
        ('Content', {'fields' : ['logo', 'heading', 'body'], 'classes' : ['collapse']}),
        ('Backgrounds', {'fields' : ['background_color', 'background_image', 'background_repeat'], 'classes' : ['collapse']}),
        ('Media', {'fields' : ['body_image', 'embed_media'], 'classes' : ['collapse']}),
        ('Forms', {'fields' : ['call_to_action_form', 'google_analytics_form'], 'classes' : ['collapse']}),
        ('Footer', {'fields' : ['footer'], 'classes' : ['collapse', 'wide']}),
    ]
    
    list_display = ( 'url', 'timestamp' )
    
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

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(LandingPageAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.editor.id:
            return False
        return True
    
    def queryset(self, request):
        if request.user.is_superuser:
            return LandingPage.objects.all()
        return LandingPage.objects.filter(editor=request.user)
    
    def get_form(self, request, obj=None, **kwargs):
        #if request.user.is_superuser:
        #    return LandingPageAdminForm
        #else:
        return LandingPageForm

admin.site.register(LandingPage, LandingPageAdmin)
admin.site.register(Layout, LayoutAdmin)


'''

NOTE:

Admin "contrib" is located here:

/usr/share/python-support/python-django/django/contrib/admin :)

'''
