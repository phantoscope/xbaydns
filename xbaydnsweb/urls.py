from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^xbaydnsweb/', include('xbaydnsweb.foo.urls')),

    # Uncomment this for admin:
     #(r'^admin/', include('django.contrib.admin.urls')),
     (r'admin/loadgen', 'xbaydnsweb.web.views.loadgenview'),
     (r'/admin/preview/', 'xbaydnsweb.web.views.preview'),
     (r'admin/smartload', 'xbaydnsweb.web.views.smartload'),
     (r'agent/create/(?P<authzcode>.*)/(?P<pubkey>.*)/$', 'xbaydnsweb.web.views.create_agent'),
     (r'slave/create/(?P<authzcode>.*)/(?P<pubkey>.*)/$', 'xbaydnsweb.web.views.create_slave'),
#     (r'agent/create/', 'xbaydnsweb.web.views.create_agent'),
#     (r'agent/create', 'xbaydnsweb.web.views.create_agent'),
     (r'', include('django.contrib.admin.urls')),
)
