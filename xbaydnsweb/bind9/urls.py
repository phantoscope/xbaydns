from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^index/', 'xbaydns.bind9.views.index'),
)
