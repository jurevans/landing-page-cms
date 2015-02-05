from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:

from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^lpg/', include('lpg.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
#    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^admin(.*)', admin.site.root),
    (r'^accounts/', include('registration.urls')),
    # Landing Page URLS
    # Expand the following Landing Page URLS to handle URL safe characters!
    (r'^(?P<landingpage_url>((\w|-)+))$', 'lpg.landingpages.views.render_page'),
    (r'^(?P<landingpage_url>((\w|-)+))/$', 'lpg.landingpages.views.render_page'),
    (r'^admin/landingpages/landingpage/(?P<object_id>[0-9]+)/preview/$','lpg.landingpages.views.preview'),
    (r'^preview/(?P<lp_id>\d+)/$', 'lpg.landingpages.views.preview'),
    # DEFAULT INDEX
    (r'^', 'lpg.landingpages.views.index'),
    #(r'^$', direct_to_template,
    #        { 'template': 'index.html' }, 'index'),
)

