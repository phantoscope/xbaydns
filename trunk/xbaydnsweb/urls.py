from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^xbaydnsweb/', include('xbaydnsweb.foo.urls')),

    # Uncomment this for admin:
     #(r'^admin/', include('django.contrib.admin.urls')),
     (r'admin/smartload', 'xbaydnsweb.web.views.smartload'),
     (r'', include('django.contrib.admin.urls')),
)
