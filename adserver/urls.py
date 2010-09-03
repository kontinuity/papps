from django.conf.urls.defaults import patterns, include
from adserver.settings import MEDIA_ROOT, DEBUG, ADMIN_MEDIA_ROOT
from adserver.partner import urls as partner_urls
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

admin.site.unregister(Group)
admin.site.unregister(Site)

urlpatterns = patterns('',
    # Example:
    # (r'^adserver/', include('adserver.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'', include(partner_urls)),
)

if DEBUG:
  urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    (r'^admin_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': ADMIN_MEDIA_ROOT}),                          
  )
