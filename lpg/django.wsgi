import os
import sys

#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
os.environ['DJANGO_SETTINGS_MODULE'] = 'lpg.settings'
sys.path.append('/home/django/landing_page_generator')
sys.path.append('/home/django/visualblaze/landing_page_generator/lpg')
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

