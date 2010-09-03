from django.conf.urls.defaults import patterns
from adserver.partner.views import login_user
from django.contrib.auth.views import logout 

urlpatterns = patterns('adserver.partner.views',
  (r'^$', 'home'),
  (r'^signup$', 'signup'),
  (r'^login$', login_user, {'template_name': 'partner/login.html'}),  
  (r'^logout$', logout),  
)
