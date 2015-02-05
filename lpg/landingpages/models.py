from django.db import models
from django.contrib.auth.models import User, UserManager, Permission
from django.contrib.auth.admin import UserAdmin
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django import forms
from PIL import Image

def get_perm(Model, perm):
    '''
    Return the permission object, for the Model
    '''
    ct = ContentType.objects.get_for_model(Model)
    return Permission.objects.get(content_type=ct,codename=perm)

'''
    Currency definition, normalized from plan cost
'''

class Currency(models.Model):
    name = models.CharField(max_length=5)
    timestamp = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.name

'''
    Plan definition, added by admin as needed
'''

class Plan(models.Model):
    name = models.CharField(max_length=50)
    number_of_pages = models.IntegerField()
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name

'''
    Account definition, created at user registration, only Admin can override, but user should
    have permissions to reset password on registration.
'''

class Account(models.Model):
    user = models.ForeignKey(User, unique=True)
    name = models.CharField(max_length=50)
    currency = models.ForeignKey(Currency)
    active = models.BooleanField()
    timestamp = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name

'''
    Domains are unique across the entire system. Domains depend on Account and Plan models.
    Affiliate codes are a placeholder for overrides in billing and will be managed in
    Google Checkout
'''

class Domain(models.Model):
    account = models.ForeignKey(Account)
    user_id = models.IntegerField(null=True, blank=True)
    domain_name = models.CharField(max_length=200, help_text='Ex. www.example.com', unique=True)
    plan = models.ForeignKey(Plan)
    affiliate_code = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.domain_name
    
class DomainAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Domain', {'fields' : ['domain_name', 'plan', 'affiliate_code']}),
    ]
    
    def queryset(self, request):
        if request.user.is_superuser:
            return Domain.objects.all()
        else:
            return Domain.objects.filter(user_id=request.user.id)
    
    def save_model(self, request, obj, form, change):
        account_object = Account.objects.get(user=request.user)
        obj.account_id = account_object.id
        obj.user_id = request.user.id
        obj.save()
       
    list_display = ('domain_name', 'account', 'timestamp')

'''
    Layout is a normalized, Admin-entered dynamic entry that serves as a pointer to a template.
    Layouts are stored in "templates/layouts/" and can pretty much be called whatever you want
    them to be. They don't mind. Layouts are not so picky; they only complain when they are
    tagged incorrectly.
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

MEDIA_CHOICES = (
    ('P', 'Upload Image'),
    ('E', 'Embed Media HTML'),
)

'''
    Landing page model definitions
'''

class LandingPage(models.Model):
    domain_name = models.ForeignKey(Domain)
    user_id = models.IntegerField(null=True, blank=True)
    url = models.SlugField(
        max_length=50,
        help_text='Choose URL slug',
    )
    title = models.CharField(
        max_length=80,
        null=True,
        blank=True,
        help_text='Enter title',
    )
    heading = models.CharField(
        max_length=80,
        help_text='Enter main heading',
    )
    body = models.TextField(help_text='Enter body content',)
    add_media = models.CharField(
        max_length=1,
        choices=MEDIA_CHOICES,
        null=True, blank=True,
        help_text='Media choices',
    )
    photo = models.ImageField(
        upload_to='uploads/images',
        null=True,
        blank=True,
        help_text='Upload image',
    )
    embed_media = models.TextField(
        null=True,
        blank=True,
        help_text='Paste embedded media code',
    )
    layout = models.ForeignKey(
        Layout,
        help_text='Select layout',
    )
    logo = models.ImageField(
        upload_to='uploads/logos',
        help_text='Upload logo',
    )
    background_color = models.CharField(
        max_length=7,
        null=True,
        blank=True,
        help_text='Select background color',
    )
    background_image = models.ImageField(
        upload_to='uploads/backgrounds',
        null=True,
        blank=True,
        help_text='Upload background image',
    )
    background_repeat = models.CharField(
        max_length=1,
        choices=BACKGROUND_CHOICES,
        null=True,
        blank=True,
        help_text='Position background image',
    )
    meta_description = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        help_text='Enter Meta Description',
    )
    meta_keywords = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        help_text='Enter Meta Keywords, separated by commas',
    )
    call_to_action_form = models.TextField(
        null=True,
        blank=True,
        help_text='Paste generated form code',
    )
    google_analytics_form = models.TextField(
        null=True,
        blank=True,
        help_text='Paste Google Analytics code',
    )
    footer = models.CharField(
        max_length=250,
        help_text='Enter footer text',
    )
    draft = models.BooleanField(help_text='Draft mode prevents this from appearing publicly.')
    timestamp = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.url
    
    @models.permalink
    def get_absolute_url(self):
        return ("lpg.landingpages.views.preview", [str(self.id)])
        
    def save(self):

        if self.photo:
            size=(425, 425)
            filename = str(self.photo.path)
            image = Image.open(filename)
            
            pw = self.photo.width
            ph = self.photo.height
            nw = size[0]
            nh = size[1]
            
            if pw > ph:
                '''
                Landscape: Width > Height
                '''
                wpercent = (nw/float(image.size[0]))
                hsize = int((float(image.size[1])*float(wpercent)))
                image = image.resize((nw,hsize), Image.ANTIALIAS)
                image.save(filename)
            else:
                '''
                Portrait: Height > Width
                '''
                hpercent = (nh/float(image.size[1]))
                wsize = int((float(image.size[0])*float(hpercent)))
                image = image.resize((wsize,nh), Image.ANTIALIAS)
                image.save(filename)
                
        super(LandingPage, self).save()
        
    def delete(self):
        '''
        Add permissions to create LandingPage when you Delete:
	This permission is removed when user creates a Landing Page and restored if deleted.
        '''

        user = User.objects.get(id=self.user_id)
        
        user.user_permissions.add(get_perm(LandingPage,
                                           LandingPage._meta.get_add_permission()))
        super(LandingPage, self).delete()
