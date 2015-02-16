from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext
from lpg.landingpages.models import LandingPage
from lpg.landingpages.models import Layout
from lpg.landingpages.models import Domain
from lpg.landingpages.models import Account
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404

def index(request):
    if request.META.get('SERVER_NAME') == 'somedomain.com': # Think about adding the Site object here, or make this a Setting
        return render_to_response('index.html')
    else:
        return HttpResponseRedirect('/accounts/login/')

def render_page(request, landingpage_url):
    try:
        # Check domain name... Perform look-up
        host = request.META.get('SERVER_NAME')
        domain = Domain.objects.get(domain_name=host)
        
        # Match object to Account to see if it is active
        account = Account.objects.get(id=domain.account_id)
        
        if(account.active):
            lps = LandingPage.objects.filter(url=landingpage_url)
            lp = lps.get(domain_name=domain)
            if lp:
                l = Layout.objects.get(name = lp.layout)
                
                if(not lp.draft):
                    return render_to_response(l.template, {'landingpage': lp, 'layout' : l})
                else:
                    raise Http404
            else:
                raise Http404
        else:
            raise Http404

    except LandingPage.DoesNotExist:
        raise Http404
    
    

'''
View code for "Preview" link
'''

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def preview(request, lp_id):
    try:
        lp = LandingPage.objects.get(pk=lp_id)
        l = Layout.objects.get(name = lp.layout)
    except LandingPage.DoesNotExist:
        raise Http404
    
    return render_to_response(l.template, {'landingpage': lp, 'layout' : l})

