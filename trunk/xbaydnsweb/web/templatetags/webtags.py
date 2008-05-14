# encoding: utf-8
"""
webtags.py

Created by QingFeng on 2008-03-23.
Copyright (c) 2008 xBayDNS Team. All rights reserved.
"""

from django import template

register = template.Library()

@register.simple_tag
def resultToHtml(results):
    print results
    html=''
    for record,idcs in results.items():
        s='%s'%record
        for idc,ips in idcs.items():
            s+='<li>%s:%s</li>'%(idc,','.join(ips))
        html+='<ul>%s</ul>'%s
    return '<ul>%s</ul>'%html

@register.simple_tag
def srvArrangeToHtml(arranges):
    html='<table>'
    for idc,services in arranges.items():
        s='<tr><td>%s</td><td></td></tr>'%idc
        for service in services:
            s+='<tr><td></td><td><input type=\'checkbox\' checked>%s</td></tr>'%service
        html+='<ul>%s</ul>'%s
    return '%s</table>'%html

@register.simple_tag
def getResultTime():
    import time,os
    from xbaydns.conf import sysconf
    CONF_FILE='%s/idcview/idcview.current'%sysconf.xbaydnsdb
    try:
        time_str = time.ctime(os.stat(CONF_FILE)[8])
    except:
        time_str = ''
    return time_str
